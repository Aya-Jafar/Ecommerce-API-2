from django.contrib.auth import get_user_model
from ninja.security import HttpBearer
from jose import jwt, JWTError
import datetime
from unicoding_project import settings

User = get_user_model()


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            user = jwt.decode(
                token=token, key=settings.SECRET_KEY, algorithms='HS256')
        except JWTError:
            return None

        if user:
            return {'pk': str(user['pk'])}
            # "created": str(user['created'])}


def create_token_for_user(user):
    token = jwt.encode({'pk': str(user.pk)},
                       key=settings.SECRET_KEY, algorithm='HS256')
    # 'created': f"{datetime.datetime.now()}"}, key=settings.SECRET_KEY, algorithm='HS256')
    return {
        'access': str(token)
    }
