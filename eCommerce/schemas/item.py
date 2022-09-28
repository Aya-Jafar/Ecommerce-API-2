from typing import Dict, List
from pydantic.networks import EmailStr
from .product import Product
from ninja import Schema



class OrderItemOut(Schema):
    id : int 
    status : str


class ItemsOut(Schema):
    id : int
    quantity : int
    total : float
    product: Product
  


class ItemIn(Schema):
    product_id : int
    quantity : int 

