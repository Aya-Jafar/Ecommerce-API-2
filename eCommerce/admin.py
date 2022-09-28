from django.contrib import admin
from .models import *


class ImageAdmin(admin.StackedInline):
    model = ProductImage


class ColorAdmin(admin.StackedInline):
    model = ProductColor


class ProductRamAndStorageAdmin(admin.StackedInline):
    model = ProductRamAndStorage


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ImageAdmin, 
        ColorAdmin, 
        ProductRamAndStorageAdmin
    ]

    class Meta:
        model = Product


admin.site.register(ProductImage)
admin.site.register(ProductColor)
admin.site.register(ProductRamAndStorage)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(Item)
admin.site.register(Favorite)
admin.site.register(Profile)
