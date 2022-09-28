from ninja import Schema
from pydantic import EmailStr, Field


class AccountIn(Schema):
    user_name : str
    email: EmailStr
    password1: str = Field(min_length=8)
    password2: str = Field(min_length=8)
    phone_number : str 


class TokenOut(Schema):
    access: str


class AccountOut(Schema):
    id : int
    user_name : str
    email: EmailStr
    phone_number : str 


class AuthOut(Schema):
    token: TokenOut
    account: AccountOut


class SigninIn(Schema):
    email: EmailStr
    password: str
