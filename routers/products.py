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
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0)
):
    conn = get_connection()
    cursor = conn.cursor()

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

    # total count
    count_query = "SELECT COUNT(*) " + base_query
    total_count = cursor.execute(count_query, params).fetchone()[0]

    # paginated data
    data_query = """
        SELECT product_id, feed_id, partner_name, sku, product_name, description,
               brand, category, price, currency, availability, created_at
    """ + base_query + " ORDER BY created_at DESC LIMIT ? OFFSET ?"

    rows = cursor.execute(data_query, params + [limit, offset]).fetchall()
    conn.close()

    items = [dict(row) for row in rows]

    return {
        "count": total_count,
        "items": items
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


