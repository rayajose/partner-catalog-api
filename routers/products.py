from fastapi import APIRouter, HTTPException, Query, Depends
from db import get_connection, q, DB_TYPE
from schemas.products import ProductResponse, ProductListResponse
from security import require_api_key

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    dependencies=[Depends(require_api_key)]
)

PRODUCT_COLUMNS = [
    "product_id",
    "feed_id",
    "partner_name",
    "sku",
    "product_name",
    "description",
    "brand",
    "category",
    "price",
    "currency",
    "availability",
    "created_at",
]


def rows_to_dicts(rows):
    if DB_TYPE == "sqlite":
        return [dict(row) for row in rows]
    return [dict(zip(PRODUCT_COLUMNS, row)) for row in rows]


def row_to_dict(row):
    if DB_TYPE == "sqlite":
        return dict(row)
    return dict(zip(PRODUCT_COLUMNS, row))


@router.get(
    "",
    response_model=ProductListResponse,
    response_model_exclude_none=True,
    summary=(
        "Retrieves products from the catalog with support for filtering, "
        "sorting, and pagination.\n\n"
        "Filtering options include:\n"
        "- partner_name\n"
        "- brand\n"
        "- category\n"
        "- availability\n\n"
        "Pagination uses a cursor-based approach for efficient large dataset traversal.\n\n"
        "Results are returned in descending order by creation time by default."
    )
)
def list_products(
    partner_name: str | None = Query(default=None,description="Filter by partner name"),
    feed_id: str | None = Query(default=None, description="Filter by feed_id"),
    sku: str | None = Query(default=None, description="Filter by sku"),
    brand: str | None = Query(default=None, description="Filter by brand"),
    category: str | None = Query(default=None, description="Filter by category"),
    availability: str | None = Query(default=None, description="Filter by availability"),
    limit: int = Query(default=10, ge=1, le=100, description="Number of results to return (default: 10, max: 100)"),
    sort_by: str = Query(default="product_id", description="Field to sort by (created_at, price, product_name, brand, category)"),
    order: str = Query(default="asc", description="Sort direction (asc, desc, default: desc)"),
    cursor: str | None = Query(
        default=None,
        description="Cursor for pagination. Use the `next_cursor` value from the previous response"
    )
):
    conn = get_connection()
    db_cursor = conn.cursor()

    try:
        allowed_sort_fields = {
            "product_id": "product_id",
            "price": "price",
            "product_name": "product_name",
            "brand": "brand",
            "category": "category",
            "created_at": "created_at",
        }

        allowed_order = {
            "asc": "ASC",
            "desc": "DESC",
        }

        if sort_by not in allowed_sort_fields:
            raise HTTPException(
                status_code=400,
                detail="Invalid sort_by value. Allowed values: product_id, price, product_name, brand, category, created_at."
            )

        if order not in allowed_order:
            raise HTTPException(
                status_code=400,
                detail="Invalid order value. Allowed values: asc, desc."
            )

        if cursor and sort_by != "product_id":
            raise HTTPException(
                status_code=400,
                detail="Cursor pagination is currently supported only with sort_by=product_id."
            )

        sort_column = allowed_sort_fields[sort_by]
        sort_direction = allowed_order[order]
        secondary_order = sort_direction if sort_by == "product_id" else "ASC"

        base_query = """
            FROM products
            WHERE 1=1
        """
        params = []

        if partner_name:
            base_query += " AND partner_name = ?"
            params.append(partner_name)

        if feed_id:
            base_query += " AND feed_id = ?"
            params.append(feed_id)

        if sku:
            base_query += " AND sku = ?"
            params.append(sku)

        if brand:
            base_query += " AND brand = ?"
            params.append(brand)

        if category:
            base_query += " AND category = ?"
            params.append(category)

        if availability:
            base_query += " AND availability = ?"
            params.append(availability)

        if cursor:
            cursor_operator = ">" if order == "asc" else "<"
            base_query += f" AND product_id {cursor_operator} ?"
            params.append(cursor)

        count_query = q("SELECT COUNT(*) " + base_query)
        count_row = db_cursor.execute(count_query, params).fetchone()
        total_count = count_row[0] if count_row else 0

        data_query = q(f"""
            SELECT product_id, feed_id, partner_name, sku, product_name, description,
                   brand, category, price, currency, availability, created_at
            {base_query}
            ORDER BY {sort_column} {sort_direction}, product_id {secondary_order}
            LIMIT ?
        """)

        rows = db_cursor.execute(data_query, params + [limit + 1]).fetchall()

        has_more = len(rows) > limit
        rows = rows[:limit]

        items = rows_to_dicts(rows)

        response = {
            "count": total_count,
            "items": items,
        }

        if has_more and items:
            response["next_cursor"] = items[-1]["product_id"]

        return response

    finally:
        conn.close()


@router.get(
    "/by-feed/{feed_id}",
    response_model=ProductListResponse,
    response_model_exclude_none=True,
    summary="List products for a feed"
)
def list_products_by_feed(feed_id: str):
    conn = get_connection()
    db_cursor = conn.cursor()

    try:
        rows = db_cursor.execute(q("""
            SELECT product_id, feed_id, partner_name, sku, product_name, description,
                   brand, category, price, currency, availability, created_at
            FROM products
            WHERE feed_id = ?
            ORDER BY product_id ASC
        """), (feed_id,)).fetchall()

        items = rows_to_dicts(rows)

        return {
            "count": len(items),
            "items": items,
        }

    finally:
        conn.close()


@router.get("/{product_id}", response_model=ProductResponse, summary="Get product by ID")
def get_product(product_id: str):
    conn = get_connection()
    db_cursor = conn.cursor()

    try:
        row = db_cursor.execute(q("""
            SELECT product_id, feed_id, partner_name, sku, product_name, description,
                   brand, category, price, currency, availability, created_at
            FROM products
            WHERE product_id = ?
        """), (product_id,)).fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Product not found.")

        return row_to_dict(row)

    finally:
        conn.close()