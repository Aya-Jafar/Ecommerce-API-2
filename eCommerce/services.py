'''
A file for some helper functions
'''

from datetime import datetime
from django.contrib.auth import get_user_model
from .models import Favorite, Item

User = get_user_model()



def check_expire_date(request):
    '''
    Check if the user is authorized based on his login date
    '''
    # Get the date of the last time the user logged in 
    created = datetime.strptime(request.auth['created'], '%Y-%m-%d %H:%M:%S.%f')
    # if the current date - the date of the last login exceed 7 days -> the user is not authorized and user should login again
    if int(datetime.now().day - created.day) < 7:
        return True
    return False



def is_favourite(product, user_id):
    try:
        if Favorite.objects.get(product__id=product.id, user__id=user_id) \
                in User.objects.get(id=user_id).favorites.all():
            is_favourite = True

    except Favorite.DoesNotExist:
        is_favourite = False

    return is_favourite


def handle_products(all_products, request):
    result = []
    for product in all_products:
        result.append(product.__dict__)
        convert_dtypes(product)
        product.__dict__['is_favourite'] = is_favourite(product, request.auth['pk'])
    return result


def handle_product(product, request):
    convert_dtypes(product)
    product.__dict__['is_favourite'] = is_favourite(product, request.auth['pk'])


def convert_dtypes(product):
    product.__dict__['colors']   = list(product.colors.all())
    product.__dict__['rams_and_storage'] = list(product.rams_and_storage.all())
    product.__dict__['product_images']  = list(product.product_images.all())

