from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    category: str
    price: float
    reorder_level: int

class ProductUpdate(BaseModel):
    name: str
    category: str
    price: float
    reorder_level: int