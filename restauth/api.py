from django.contrib.auth import get_user_model
from ninja import Router
from eCommerce.schemas.product import FourOFour
from rest_framework import status
from .authorization import create_token_for_user
from .schemas import AccountIn, AuthOut, SigninIn


auth_router = Router(tags=['Auth'])
User = get_user_model()


@auth_router.post('signup/', response={
    201: AuthOut,
    404: FourOFour,
})
def signup(request, account_in: AccountIn):
    if account_in.password1 != account_in.password2:
        return status.HTTP_404_NOT_FOUND, {'detail': 'Passwords should look alike'}

    try:
        User.objects.get(email=account_in.email)
    except User.DoesNotExist:
        new_user = User.objects.create_user(
            user_name=account_in.user_name,
            email=account_in.email,
            password=account_in.password1,
            phone_number=account_in.phone_number
        )

        token = create_token_for_user(new_user)

        return status.HTTP_201_CREATED, {
            'token': token,
            'account': new_user
        }

    return status.HTTP_404_NOT_FOUND, {'message': 'Email is taken'}


@auth_router.post('signin/', response={
    200: AuthOut,
    404: FourOFour
})
def signin(request, signin_in: SigninIn):
    try:
        user = User.objects.get(email=signin_in.email)
    except User.DoesNotExist:
        user = None

    else:
        if user.check_password(signin_in.password):
            token = create_token_for_user(user)

            return {
                'token': token,
                'account': user
            }

    if not user:
        return status.HTTP_404_NOT_FOUND, {'message': 'User is not registered'}
