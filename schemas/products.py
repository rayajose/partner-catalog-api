from __future__ import annotations
from typing import Optional
from pydantic import BaseModel


class ProductResponse(BaseModel):
    product_id: str
    feed_id: str
    partner_name: str
    sku: Optional[str] = None
    product_name: str
    description: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    availability: Optional[str] = None
    created_at: str


class ProductListResponse(BaseModel):
    count: int
    items: list[ProductResponse]