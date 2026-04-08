from fastapi import APIRouter, HTTPException, Query, Depends
from db import get_connection
from schemas.products import ProductResponse, ProductListResponse
from security import require_api_key

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    dependencies=[Depends(require_api_key)]
)


@router.get("", response_model=ProductListResponse, summary="List products")
def list_products(
    partner_name: str | None = Query(default=None),
    feed_id: str | None = Query(default=None),
    sku: str | None = Query(default=None),
    brand: str | None = Query(default=None),
    category: str | None = Query(default=None),
    availability: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=500),
    sort_by: str = Query(default="created_at"),
    order: str = Query(default="desc"),
    cursor: str | None = Query(
        default=None,
        description="Pagination cursor in the format created_at|product_id"
    )
):
    conn = get_connection()
    db_cursor = conn.cursor()

    allowed_sort_fields = {
        "created_at": "created_at",
        "price": "price",
        "product_name": "product_name",
        "brand": "brand",
        "category": "category",
    }

    allowed_order = {
        "asc": "ASC",
        "desc": "DESC",
    }

    if sort_by not in allowed_sort_fields:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Invalid sort_by value. Allowed values: created_at, price, product_name, brand, category."
        )

    if order not in allowed_order:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Invalid order value. Allowed values: asc, desc."
        )

    # Keep cursor pagination limited to the default stable sort
    if cursor and not (sort_by == "created_at" and order == "desc"):
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Cursor pagination is currently supported only with sort_by=created_at and order=desc."
        )

    sort_column = allowed_sort_fields[sort_by]
    sort_direction = allowed_order[order]

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

    # Cursor filter for created_at DESC, product_id ASC tie-breaker
    # "after this item" in descending created_at order means:
    # created_at < cursor_created_at
    # OR same created_at and product_id > cursor_product_id
    if cursor:
        try:
            cursor_created_at, cursor_product_id = cursor.split("|", 1)
        except ValueError:
            conn.close()
            raise HTTPException(
                status_code=400,
                detail="Invalid cursor format. Expected created_at|product_id."
            )

        base_query += """
            AND (
                created_at < ?
                OR (created_at = ? AND product_id > ?)
            )
        """
        params.extend([cursor_created_at, cursor_created_at, cursor_product_id])

    count_query = "SELECT COUNT(*) " + base_query
    total_count = db_cursor.execute(count_query, params).fetchone()[0]

    data_query = f"""
        SELECT product_id, feed_id, partner_name, sku, product_name, description,
               brand, category, price, currency, availability, created_at
    """ + base_query + f"""
        ORDER BY {sort_column} {sort_direction}, product_id ASC
        LIMIT ?
    """

    rows = db_cursor.execute(data_query, params + [limit]).fetchall()
    conn.close()

    items = [dict(row) for row in rows]

    next_cursor = None
    if items:
        last_item = items[-1]
        next_cursor = f"{last_item['created_at']}|{last_item['product_id']}"

    return {
        "count": total_count,
        "items": items,
        "next_cursor": next_cursor
    }

@router.get("/by-feed/{feed_id}", response_model=ProductListResponse, summary="List products for a feed")
def list_products_by_feed(feed_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    rows = cursor.execute("""
        SELECT product_id, feed_id, partner_name, sku, product_name, description,
               brand, category, price, currency, availability, created_at
        FROM products
        WHERE feed_id = ?
        ORDER BY created_at DESC
    """, (feed_id,)).fetchall()

    conn.close()

    items = [dict(row) for row in rows]
    return {"items": items, "count": len(items)}

@router.get("/{product_id}", response_model=ProductResponse, summary="Get product by ID")
def get_product(product_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    row = cursor.execute("""
        SELECT product_id, feed_id, partner_name, sku, product_name, description,
               brand, category, price, currency, availability, created_at
        FROM products
        WHERE product_id = ?
    """, (product_id,)).fetchone()

    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Product not found.")

    return dict(row)


