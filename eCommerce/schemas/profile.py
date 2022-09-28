from ninja import Schema
from pydantic.networks import EmailStr


class DataIn(Schema):
    user_name: str
    email : EmailStr
    address: str

class ProfileOut(DataIn):
    pass
