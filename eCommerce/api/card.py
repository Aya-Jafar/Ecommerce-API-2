from eCommerce.services import handle_related_objects
from restauth.authorization import AuthBearer
from eCommerce.schemas.item import ItemIn
from django.contrib.auth import get_user_model
from rest_framework import status
from eCommerce.schemas.cart import CardQntOut, CartOut, TotalCardOut, MessageOut, OrderIn
from typing import List
from ninja import Router
from ..models import Order, Item, Product


card_router = Router(tags=['Card'])

User = get_user_model()


@card_router.get('view-cart/', response={
    200: CartOut,
    404: MessageOut,
}, auth=AuthBearer())
def view_cart(request):
    try:
        cart_items = Order.objects.get(
            owner__id=request.auth['pk'], is_ordered=False)

        if cart_items:
            return status.HTTP_200_OK, {
                'id': cart_items.id,
                'cart_total': cart_items.get_cart_total,
                'cart_quantity': cart_items.get_cart_quantity,
                'items': handle_related_objects(cart_items.items.all())
            }

    except Order.DoesNotExist:
        return status.HTTP_404_NOT_FOUND, {'detail': 'Your cart is empty'}


@card_router.get('get-card-total/', response={
    200: TotalCardOut,
}, auth=AuthBearer())
def get_card_total(request):
    ''' Getting the total of the items in the cart.'''
    try:
        total = Order.objects.get(
            owner__id=request.auth['pk'],
            is_ordered=False).get_cart_total

        return status.HTTP_200_OK, {'total': total}

    except Order.DoesNotExist:
        return status.HTTP_200_OK, {'total': 0}


@card_router.get('get-total-card-quantity/', response={
    200: CardQntOut,
}, auth=AuthBearer())
def get_cart_quantity(request):
    '''Getting the total quantity of the items in the cart'''

    try:
        total_qnt = Order.objects.get(
            owner__id=request.auth['pk'], is_ordered=False).get_cart_quantity

        return status.HTTP_200_OK, {'total_qnt': total_qnt}

    except Order.DoesNotExist:
        return status.HTTP_200_OK, {'total_qnt': 0}


@card_router.post('add-to-card/', response={
    200: MessageOut,
    400: MessageOut,
    404: MessageOut
}, auth=AuthBearer())
def add_to_card(request, item_in: ItemIn):
    '''Checking if the item is in the cart and if it is, it will increase the quantity of the item. 
    If it is not in the cart it will create new item and add it to the cart'''

    try:
        item = Item.objects.get(
            product_id=item_in.product_id,
            user=User.objects.get(id=request.auth['pk']),
            is_ordered=False)

        if item_in.quantity > 0:
            item.quantity += item_in.quantity
            item.save()
            # print(item)
            return status.HTTP_200_OK, {
                'detail': 'Item updated successfully'
            }

        return status.HTTP_400_BAD_REQUEST, {
            'detail': 'Quantity Value Must be Greater Than Zero'
        }

    except Item.DoesNotExist:
        try:
            product = Product.objects.get(id=item_in.product_id)
            item = Item.objects.create(
                **item_in.dict(),
                is_ordered=False,
                user=User.objects.get(id=request.auth['pk']))

        except Product.DoesNotExist:
            return status.HTTP_404_NOT_FOUND, {
                'detail': f'Product with id {item_in.product_id} does not exist'
            }

        if item_in.quantity < 1:
            return status.HTTP_400_BAD_REQUEST, {
                'detail': 'Quantity Value Must be Greater Than Zero'
            }
        try:
            Order.objects.get(
                owner__id=request.auth['pk'], is_ordered=False).items.add(item)

            return status.HTTP_200_OK, {
                'detail': 'Item added successfully'
            }

        except Order.DoesNotExist:
            res = create_update_order(request)
            # order = Order.objects.create(
            #     owner=User.objects.get(id=request.auth['pk']), status='Order Taken', is_ordered=False
            # )
            # item = Item.objects.create(
            #     **item_in.dict(),
            #     is_ordered=False,
            #     user=User.objects.get(id=request.auth['pk'])
            # )
            # order.items.add(item)
            return res


def create_update_order(request):

    user = User.objects.get(id=request.auth['pk'])
    user_items = user.items.filter(is_ordered=False)

    try:
        # Getting the order that is not ordered yet and getting the product id of
        # the items in the order
        order = user.orders.prefetch_related('items').get(is_ordered=False)
        list_of_productID_in_order = [
            item['product_id'] for item in order.items.values('product_id')
        ]

        # Checking if the item is in the order and if it is, it will add the item to the order.
        # If it is not in the order it will create new item and add it to the order.

        list_of_difference_items = []
        list_of_intersection_items = [
            (item, item.quantity) if item.product_id in list_of_productID_in_order
            else list_of_difference_items.append(item.id) for item in user_items
        ]

        Item.objects.filter(
            id__in=list_of_difference_items).update(is_ordered=True)

        for item, qty in list(filter(None, list_of_intersection_items)):
            item_duplicated = order.items.get(product_id=item.product_id)
            item_duplicated.quantity = item_duplicated.quantity + qty
            item_duplicated.save()

        order.items.add(*list_of_difference_items)
        order.save()
        return status.HTTP_200_OK, {'detail': 'Card updated successfully!'}

    except Order.DoesNotExist:
        order = Order.objects.create(
            owner=user, status='Order Taken', is_ordered=False)

        order.items.set(user_items)

        order.save()
        return status.HTTP_200_OK, {'detail': 'Card Created and item added Successfully!'}


@card_router.post('Checkout/', response={
    200: MessageOut,
    404: MessageOut,
}, auth=AuthBearer())
def checkout_order(request):
    try:
        order = Order.objects.get(
            owner__id=request.auth['pk'], is_ordered=False)
        order.is_ordered = True
        order.status = 'Order is Being Prepared'
        for item in order.items.all():
            item.is_ordered = True
            item.save()
        order.save()
        return status.HTTP_200_OK, {
            'detail': 'Checkout successfully! You will recieve a message with more details'
        }

    except Order.DoesNotExist:
        return status.HTTP_404_NOT_FOUND, {'detail': 'Order Does\'nt Found'}


@card_router.delete('delete-card/{id}', response={
    200: MessageOut,
    404: MessageOut
}, auth=AuthBearer())
def delete_card(request, id: int):
    try:
        order = Order.objects.get(id=id, owner__id=request.auth['pk'])
        order.delete()
        return status.HTTP_200_OK, {'detail': 'Card has been deleted successfully!'}

    except Order.DoesNotExist:
        return status.HTTP_404_NOT_FOUND, {'detail': f'Card with id {id} does not exist'}
