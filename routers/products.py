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
    limit: int = Query(default=50, ge=1, le=500)
):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT product_id, feed_id, partner_name, sku, product_name, description,
               brand, category, price, currency, availability, created_at
        FROM products
        WHERE 1=1
    """
    params = []

    if partner_name:
        query += " AND partner_name = ?"
        params.append(partner_name)

    if feed_id:
        query += " AND feed_id = ?"
        params.append(feed_id)

    if sku:
        query += " AND sku = ?"
        params.append(sku)

    if brand:
        query += " AND brand = ?"
        params.append(brand)

    if category:
        query += " AND category = ?"
        params.append(category)

    query += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)

    rows = cursor.execute(query, params).fetchall()
    conn.close()

    items = [dict(row) for row in rows]
    return {"items": items, "count": len(items)}

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


