from eCommerce.schemas.item import ItemsOut
from ninja import Schema
from restauth.schemas import AccountOut
from typing import List
# from .product import ProductOut

class ItemOutForCard(Schema):
    product_id : int
    quantity : int


class TotalCardOut(Schema):
    total : float  


class CartOut(Schema):
    id : int
    cart_total : float
    cart_quantity : int
    items: List[ItemsOut]



class CardQntOut(Schema):
    total_qnt: int 


class MessageOut(Schema):
    detail:str 
 

class OrderIn(Schema):
    items: List[int] 


CartOut.update_forward_refs()