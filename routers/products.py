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

from fastapi import APIRouter, HTTPException, Query
from db import get_connection
from schemas.products import ProductListResponse

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=ProductListResponse, summary="List products")
def list_products(
    partner_name: str | None = Query(default=None),
    feed_id: str | None = Query(default=None),
    sku: str | None = Query(default=None),
    brand: str | None = Query(default=None),
    category: str | None = Query(default=None),
    availability: str | None = Query(default=None),
    limit: int = Query(default=10, ge=1, le=100),
    sort_by: str = Query(default="product_id"),
    order: str = Query(default="asc"),
    cursor: str | None = Query(
        default=None,
        description="Pagination cursor. Use the last product_id returned from the previous page."
    )
):
    conn = get_connection()
    db_cursor = conn.cursor()

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
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Invalid sort_by value. Allowed values: product_id, price, product_name, brand, category, created_at."
        )

    if order not in allowed_order:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Invalid order value. Allowed values: asc, desc."
        )

    if cursor and sort_by != "product_id":
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Cursor pagination is currently supported only with sort_by=product_id."
        )

    sort_column = allowed_sort_fields[sort_by]
    sort_direction = allowed_order[order]

    base_query = """
        FROM products
        WHERE 1=1
    """
    params: list = []

    if partner_name:
        base_query += " AND partner_name = %s"
        params.append(partner_name)

    if feed_id:
        base_query += " AND feed_id = %s"
        params.append(feed_id)

    if sku:
        base_query += " AND sku = %s"
        params.append(sku)

    if brand:
        base_query += " AND brand = %s"
        params.append(brand)

    if category:
        base_query += " AND category = %s"
        params.append(category)

    if availability:
        base_query += " AND availability = %s"
        params.append(availability)

    if cursor:
        cursor_operator = ">" if order == "asc" else "<"
        base_query += f" AND product_id {cursor_operator} %s"
        params.append(cursor)

    count_query = "SELECT COUNT(*) " + base_query
    db_cursor.execute(count_query, params)
    count_row = db_cursor.fetchone()
    total_count = count_row[0]

    data_query = f"""
        SELECT product_id, feed_id, partner_name, sku, product_name, description,
               brand, category, price, currency, availability, created_at
        {base_query}
        ORDER BY {sort_column} {sort_direction}, product_id ASC
        LIMIT %s
    """

    db_cursor.execute(data_query, params + [limit])
    rows = db_cursor.fetchall()
    conn.close()

    items = rows_to_dicts(rows)

    next_cursor = None
    if items:
        next_cursor = items[-1]["product_id"]

    return {
        "count": total_count,
        "items": items,
        "next_cursor": next_cursor
    }

@router.get("/by-feed/{feed_id}", response_model=ProductListResponse, summary="List products for a feed")
def list_products_by_feed(feed_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    rows = cursor.execute(q("""
        SELECT product_id, feed_id, partner_name, sku, product_name, description,
               brand, category, price, currency, availability, created_at
        FROM products
        WHERE feed_id = ?
        ORDER BY created_at DESC
    """), (feed_id,)).fetchall()

    conn.close()

    items = rows_to_dicts(rows)
    return {"items": items, "count": len(items)}


@router.get("/{product_id}", response_model=ProductResponse, summary="Get product by ID")
def get_product(product_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    row = cursor.execute(q("""
        SELECT product_id, feed_id, partner_name, sku, product_name, description,
               brand, category, price, currency, availability, created_at
        FROM products
        WHERE product_id = ?
    """), (product_id,)).fetchone()

    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Product not found.")

    return row_to_dict(row)