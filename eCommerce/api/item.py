from eCommerce.services import convert_dtypes
from restauth.authorization import AuthBearer
from django.contrib.auth import get_user_model
from eCommerce.schemas.cart import MessageOut, TotalCardOut
from eCommerce.schemas.product import FourOFour
from rest_framework import status
from eCommerce.schemas.item import ItemsOut
from typing import List
from ninja import Router
from ..models import Item, Order


item_router = Router(tags=['Items inside card'])

User = get_user_model()


@item_router.get('get-items/', response={
    200: List[ItemsOut],
    404: FourOFour
}, auth=AuthBearer())
def get_items_in_card(request):
    try:
        items = Item.objects.select_related('product', 'user').filter(user=User.objects.get(
            id=request.auth['pk']), is_ordered=False)
        result  = []
        for i in items:
            convert_dtypes(i.product)
            result.append({
                'id':i.id,
                'quantity':i.quantity,
                'total':i.get_item_total,
                'product': i.product.__dict__,
            })

        if items:
            return status.HTTP_200_OK, result

        return status.HTTP_404_NOT_FOUND, {'message': 'Card is empty'}

    except Order.DoesNotExist:
        return status.HTTP_404_NOT_FOUND, {'message': 'Card does not exist'}



@item_router.get('get-item-total/', response={
    200: TotalCardOut,
    404: FourOFour
}, auth=AuthBearer())
def get_item_total(request, item_id: int):
    try:
        item_total = Item.objects.get(
            id=item_id,
            user=User.objects.get(id=request.auth['pk']),
            is_ordered=False).get_item_total

        return status.HTTP_200_OK, {'total': item_total}

    except Item.DoesNotExist:
        return status.HTTP_404_NOT_FOUND, {'message': 'Item does not exist'}


@item_router.post('item-increase-quantity/{id}', response={
    200: MessageOut,
    404: MessageOut
}, auth=AuthBearer())
def increase_item_quantity(request, id: int):
    try:
        item = Item.objects.get(id=id, user=User.objects.get(
            id=request.auth['pk']), is_ordered=False)

        item.quantity += 1
        item.save()

        return status.HTTP_200_OK, {
            'detail': 'Item quantity increased successfully!'
        }
    except Item.DoesNotExist:
        return status.HTTP_404_NOT_FOUND, {'detail': f'Item with id {id} does not exist'}


@item_router.post('reduce-quantity/{id}', response={
    200: MessageOut,
    404: MessageOut
}, auth=AuthBearer())
def reduce_item_quantity(request, id: int):
    try:
        item = Item.objects.get(id=id, user=User.objects.get(
            id=request.auth['pk']), is_ordered=False)

        if item.quantity == 1:
            item.delete()
            return status.HTTP_200_OK, {'detail': 'Item deleted!'}
        item.quantity -= 1
        item.save()

        return status.HTTP_200_OK, {
            'detail': 'Item quantity reduced successfully!'
        }
    except Item.DoesNotExist:
        return status.HTTP_404_NOT_FOUND, {'detail': f'Item with id {id} does not exist'}


@item_router.delete('delete-item/{id}', response={
    200: MessageOut,
    404: MessageOut
}, auth=AuthBearer())
def delete_item(request, id: int):
    try:
        item = Item.objects.get(id=id, user=User.objects.get(
            id=request.auth['pk']), is_ordered=False)
        item.delete()
        return status.HTTP_200_OK, {'detail': 'Item has been deleted successfully!'}

    except Item.DoesNotExist:
        return status.HTTP_404_NOT_FOUND, {'detail': f'Item with id {id} does not exist'}
