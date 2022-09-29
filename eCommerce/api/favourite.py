from eCommerce.services import check_expire_date
from typing import List
from django.contrib.auth import get_user_model
from eCommerce.schemas.product import FavProductOut
from eCommerce.models import Favorite, Product
from ninja import Router
from eCommerce.schemas.cart import MessageOut
from restauth.authorization import AuthBearer
from rest_framework import status


fav_router = Router(tags=['Favourites'])


User = get_user_model()


@fav_router.get('view-favourites/', response={
    200: List[FavProductOut],
    404: MessageOut
},auth=AuthBearer())
def favourite_products(request):
    '''Getting all the favourite products of the user.'''
    if check_expire_date(request):
        fav_products = Favorite.objects.select_related('user', 'product').filter(
            user=User.objects.get(id=request.auth['pk']))
        
        if fav_products:
            return status.HTTP_200_OK,fav_products

        return status.HTTP_404_NOT_FOUND, {'detail': 'No favourite products found'}

    return status.HTTP_404_NOT_FOUND, {'detail': 'Not authorized'}



@fav_router.post('mark-as-favourite/', response={
    200: MessageOut,
    400: MessageOut,
    404: MessageOut
},auth=AuthBearer())
def mark_as_favourite(request, id: int):
    '''Checking if the product is already a favourite. If it is, it returns a 400 error. 
    If it is not, it creates a new favourite product if the product exists'''
    if check_expire_date(request):
        try:
            fav_product = Favorite.objects.get(
                product=Product.objects.get(id=id),
                user=User.objects.get(id=request.auth['pk']))

            if fav_product in User.objects.get(id=request.auth['pk']).favorites.all():
                return status.HTTP_400_BAD_REQUEST, {'detail': f'Product is already a favourite'}

        except Product.DoesNotExist:
            return status.HTTP_404_NOT_FOUND, {'detail': f'Product with id {id} does not exist'}

        except Favorite.DoesNotExist:
            fav_product = Favorite.objects.create(
                product=Product.objects.get(id=id),
                user=User.objects.get(id=request.auth['pk']))

            User.objects.get(id=request.auth['pk']).favorites.add(fav_product)

            return status.HTTP_404_NOT_FOUND, {'detail': f'Product with id {id} is favourite now'}

    return status.HTTP_404_NOT_FOUND, {'detail': 'Not authorized'}



@fav_router.delete('delete-favourite/', response={
    200: MessageOut,
    404: MessageOut
},auth=AuthBearer())
def delete_fav(request, id: int):
    '''Deleting a favourite product if it exists'''
    if check_expire_date(request):
        try:
            fav_product = Favorite.objects.get(
                id=id,
                user=User.objects.get(id=request.auth['pk']))

            fav_product.delete()
            return status.HTTP_200_OK, {'detail': 'Favourite product has been deleted successfully!'}

        except Favorite.DoesNotExist:
            return status.HTTP_404_NOT_FOUND, {'detail': 'Product is not a favourite'}

    return status.HTTP_404_NOT_FOUND, {'detail': 'Not authorized'}


@fav_router.delete('delete-all-favourites/', response={
    200: MessageOut,
    404: MessageOut
},auth=AuthBearer())
def delete_all(request):
    if check_expire_date(request):
        fav_products = Favorite.objects.select_related('user', 'product').filter(
            user=User.objects.get(id=request.auth['pk']))

        if fav_products:
            for fav in fav_products.all():
                fav.delete()

            return status.HTTP_200_OK, {'detail': 'All favourite products has been deleted successfully!'}
        else:
            return status.HTTP_404_NOT_FOUND, {'detail': 'No favourite products found'}
            
    return status.HTTP_404_NOT_FOUND, {'detail': 'Not authorized'}
