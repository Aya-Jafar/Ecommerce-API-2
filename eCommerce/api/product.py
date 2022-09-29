
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from restauth.authorization import AuthBearer
from rest_framework import status
from eCommerce.schemas.product import ProductOut, FourOFour, ImgOut
from ..models import Item, Order, Product, ProductImage
from ..choices import ProductBrand, ProductCatogary
from typing import List
from ninja import Router
from ..services import handle_product, handle_products, check_expire_date


product_router = Router(tags=['Product'])


User = get_user_model()


@product_router.get('get-all/', response={
    200:List[ProductOut],
    404:FourOFour
}, auth=AuthBearer())
def get_all_products(request):
    if check_expire_date(request):
        all_products = Product.objects.order_by('-id')
        result = handle_products(all_products, request)
        return result
    return status.HTTP_404_NOT_FOUND, {'message': 'Not authorized'}


@product_router.get('get-product-by-id/', response={
    200: ProductOut,
    404: FourOFour
}, auth=AuthBearer())
def get_product_by_id(request, id: int):
    if check_expire_date(request):
        try:
            product = Product.objects.get(id=id)
            handle_product(product, request)
            return status.HTTP_200_OK, product

        except Product.DoesNotExist:
            return status.HTTP_404_NOT_FOUND, {'message': f'Product with id {id} does not exist'}

    return status.HTTP_404_NOT_FOUND, {'message': 'Not authorized'}


@product_router.get('get-product-by-name/', response={
    200: ProductOut,
    404: FourOFour
}, auth=AuthBearer())
def get_product_by_name(request, name: str):
    if check_expire_date(request):
        try:
            product = Product.objects.get(name=name)
            handle_product(product, request)
            return status.HTTP_200_OK, product
        except Product.DoesNotExist:
            return status.HTTP_404_NOT_FOUND, {'message': f'{name} product does not exist'}

    return status.HTTP_404_NOT_FOUND, {'message': 'Not authorized'}


@product_router.get('filter-phones/', response={
    200: List[ProductOut],
    404: FourOFour
}, auth=AuthBearer())
def filter_phones(request):
    if check_expire_date(request):
        filtered = Product.objects.order_by('-id').filter(catogary='Phones')
        if filtered:
            filtered = handle_products(filtered, request)
            return status.HTTP_200_OK, filtered

        return status.HTTP_404_NOT_FOUND, {'message': 'No products in Phones catogary'}

    return status.HTTP_404_NOT_FOUND, {'message': 'Not authorized'}


@product_router.get('filter-laptops/', response={
    200: List[ProductOut],
    404: FourOFour
}, auth=AuthBearer())
def filter_laptops(request):
    if check_expire_date(request):
        filtered = Product.objects.order_by('-id').filter(catogary='Laptops')
        if filtered:
            filtered = handle_products(filtered, request)
            return status.HTTP_200_OK, filtered

        return status.HTTP_404_NOT_FOUND, {'message': 'No products in Laptops catogary'}

    return status.HTTP_404_NOT_FOUND, {'message': 'Not authorized'}


@product_router.get('filter-tablets/', response={
    200: List[ProductOut],
    404: FourOFour
}, auth=AuthBearer())
def filter_tablets(request):
    if check_expire_date(request):
        filtered = Product.objects.order_by('-id').filter(catogary='Tablets')
        if filtered:
            filtered = handle_products(filtered, request)
            return status.HTTP_200_OK, filtered

        return status.HTTP_404_NOT_FOUND, {'message': 'No products in Tablets catogary'}

    return status.HTTP_404_NOT_FOUND, {'message': 'Not authorized'}


@product_router.get('filter-desctop-pc/', response={
    200: List[ProductOut],
    404: FourOFour
}, auth=AuthBearer())
def filter_pc(request):
    if check_expire_date(request):
        filtered = Product.objects.order_by('-id').filter(catogary='Desktop pc')
        if filtered:
            filtered = handle_products(filtered, request)
            return status.HTTP_200_OK, filtered

        return status.HTTP_404_NOT_FOUND, {'message': 'No products in Desktop pc catogary'}

    return status.HTTP_404_NOT_FOUND, {'message': 'Not authorized'}


@product_router.get('get-trending-products/', response={
    200: List[ProductOut],
    404: FourOFour
}, auth=AuthBearer())
def filter_trending_products(request):
    if check_expire_date(request):
        trending_products = Product.objects.order_by('-id').filter(is_trending_now=True)
        if trending_products:
            trending_products = handle_products(trending_products, request)
            return status.HTTP_200_OK, trending_products
        return status.HTTP_404_NOT_FOUND, {'message': 'No trending products found'}

    return status.HTTP_404_NOT_FOUND, {'message': 'Not authorized'}


@product_router.get('get-best-selling-products/', response={
    200: List[ProductOut],
    404: FourOFour
}, auth=AuthBearer())
def filter_best_selling_products(request):
    if check_expire_date(request):
        best_selling = Product.objects.order_by(
            '-id').filter(is_best_selling=True)
        if best_selling:
            best_selling = handle_products(best_selling, request)
            return status.HTTP_200_OK, best_selling
        return status.HTTP_404_NOT_FOUND, {'message': 'No best selling products found'}

    return status.HTTP_404_NOT_FOUND, {'message': 'Not authorized'}


@product_router.get('filter-by-brand/', response={
    200: List[ProductOut],
    404: FourOFour
}, auth=AuthBearer())
def filter_by_brand(request, to_filter_by: str):
    if check_expire_date(request):
        choices = [i[0] for i in ProductBrand.choices]
        if to_filter_by in choices:
            filtered = Product.objects.filter(brand__iexact=to_filter_by)
            filtered = handle_products(filtered, request)
            return status.HTTP_200_OK, filtered

        return status.HTTP_404_NOT_FOUND, {'message': f'No brand named {to_filter_by}'}

    return status.HTTP_404_NOT_FOUND, {'message': 'Not authorized'}


@product_router.get('filter-by-price/', response={
    200: List[ProductOut],
    404: FourOFour
}, auth=AuthBearer())
def filter_by_price(request, min: int, max: int):
    if check_expire_date(request):
        filtered = Product.objects.filter(price__in=range(min, max+1))
        if filtered:
            filtered = handle_products(filtered, request)
            return status.HTTP_200_OK, filtered

        return status.HTTP_404_NOT_FOUND, {'message': f'No products found with price range {min} - {max}'}

    return status.HTTP_404_NOT_FOUND, {'message': 'Not authorized'}


@product_router.post('buy-now/', response={
    200: FourOFour,
    404: FourOFour
}, auth=AuthBearer())
def buy_now(request, product_id: int):
    if check_expire_date(request):
        item = Item.objects.create(
            is_ordered=True,
            quantity=1,
            product=Product.objects.get(id=product_id),
            user=User.objects.get(id=request.auth['pk'])
        )
        try:
            order = Order.objects.get(
                is_ordered=True, owner__id=request.auth['pk'])
            order.items.add(item)
            return status.HTTP_200_OK, {'message': 'Product is ordered successfully'}

        except Order.DoesNotExist:
            order = Order.objects.create(
                is_ordered=True, owner__id=request.auth['pk'])
            order.items.add(item)
            return status.HTTP_200_OK, {'message': 'Product is ordered successfully'}

    return status.HTTP_404_NOT_FOUND, {'message': 'Not authorized'}


@product_router.get('product-images/', response={
    200:List[ImgOut],
    404: FourOFour
}, auth=AuthBearer())
def get_product_images(request):
    if check_expire_date(request):
        return ProductImage.objects.select_related('product').all()
    return status.HTTP_404_NOT_FOUND, {'message': 'Not authorized'}
