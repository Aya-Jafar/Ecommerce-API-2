from restauth.authorization import AuthBearer
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from eCommerce.api import product_router, card_router, item_router, fav_router, profile_router
from restauth.api import auth_router
from django.conf import settings
from django.conf.urls.static import static


api = NinjaAPI(
    title='Elecronic e-Commerce API',
)


api.add_router('product/', product_router)
api.add_router('auth/', auth_router)
api.add_router('Card/', card_router)
api.add_router('Items/', item_router)
api.add_router('Favourites/', fav_router)
api.add_router('Profile/', profile_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
