from django.contrib.auth import get_user_model
from django.db import models
from .choices import ProductCatogary, ProductBrand, Status, Gender, City, ProductSystem
from django.db.models.signals import pre_delete, post_save, pre_save
from django.dispatch import receiver
from PIL import Image
from colorfield.fields import ColorField


User = get_user_model()


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )
    catogary = models.CharField(
        max_length=255,
        choices=ProductCatogary.choices
    )
    brand = models.CharField(
        max_length=255,
        choices=ProductBrand.choices
    )
    rate = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )
    cpu = models.CharField(max_length=255)
    system = models.CharField(
        max_length=255,
        choices=ProductSystem.choices,
    )

    is_best_selling = models.BooleanField(default=False)
    is_trending_now = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ProductRamAndStorage(models.Model):
    '''One product has many ram and storages 
       in the format #/# GB
    '''
    name = models.CharField(max_length=8)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='rams_and_storage'
    )

    def __str__(self):
        return self.name


class Order(models.Model):  # Card
    '''Container for the ordered items
       Many cards - many items
    '''
    owner = models.ForeignKey(
        User,
        related_name='orders',
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=255,
        choices=Status.choices
    )
    is_ordered = models.BooleanField(
        default=False)  # become true when checkout
    items = models.ManyToManyField(
        'Item',
        related_name='order'
    )

    def __str__(self):
        return f'{self.owner.user_name}\'s order'

    @property
    def get_cart_total(self):
        '''Returns the total price of the card'''
        items = self.items.all()
        total = sum([item.get_item_total for item in items])
        return total

    @property
    def get_cart_quantity(self):
        '''Returns the total quantity of the card'''
        items = self.items.all()
        total = sum([item.quantity for item in items])
        return total


class Item(models.Model):
    '''Ordered products inside user's card'''
    user = models.ForeignKey(
        User,
        related_name='items',
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product'
    )

    quantity = models.IntegerField(default=0)

    is_ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.product.name} - {self.user}'

    @property
    def get_item_total(self):
        '''Returns the total price of one item'''
        total = self.product.price * self.quantity
        return total

    @receiver(pre_delete, sender=Order)
    def delete_items(sender, instance, **kwargs):
        '''Deletes all related items when Card is deleted'''
        for item in instance.items.all():
            item.delete()

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'


class Favorite(models.Model):
    '''A model for storing Favorite products and user that liked it.'''
    user = models.ForeignKey(
        User,
        related_name='favorites',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name='favorites',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.product.name} - {self.user.user_name}'


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products_images/')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_images'
    )

    def __str__(self):
        return f'{self.product.name} \'s image'

    class Meta:
        verbose_name = 'Product image'
        verbose_name_plural = 'Product images'


    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            # img = img.resize((output_size), Image.ANTIALIAS)
            img.save(self.image.path)


class ProductColor(models.Model):
    ''' 
    One product can have many colors.
    colors are stored in HEX format using colorfield package
    '''
    name = ColorField()
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='colors',
    )

    def __str__(self):
        return self.name


@receiver(pre_save, sender=ProductColor)
def flutter_color_format(sender, instance, **kwargs):
    ''' 
    A signal that is used to format the color name to
    a flutter format.
    '''
    instance.name = instance.name.replace('#', '')
    instance.name = f'0xff{instance.name}'


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    # image = models.ImageField(upload_to='profile_images/')

    # gender = models.CharField(
    #     max_length=50, choices=Gender.choices, default='Male')

    address = models.CharField(
        max_length=50,
        choices=sorted(City.choices),
        default='Baghdad'
    )

    def __str__(self):
        return f'{self.user.user_name}'

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        '''
        A signal that creates user Profile once a user has been created 
        and only if the user is not staff
        '''
        if not instance.is_staff:
            if created:
                Profile.objects.create(user=instance)
                instance.profile.save()
