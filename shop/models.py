from email.mime import image
from enum import unique
from unicodedata import name
from django.db import models
from django_extensions.db.fields import RandomCharField
from django_extensions.db.models import *
from django.contrib.auth import get_user_model
import requests

# from shop.forms import PAYMENT_CHOICES


PAYMENT_CHOICES = (
    ('c', "Credit card"),
    ('d', "Pay on delivery")
)


def save_item_image_file_path(self, image):
    lenn = self.item.images.count()
    return f'shop/images/{self.item.id}/image_{lenn}.png'


User = get_user_model()

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True, default='Others')
    slug = AutoSlugField(populate_from='title')

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'


class Item(TitleSlugDescriptionModel):
    id = RandomCharField(length=8, unique=True, primary_key=True)
    price = models.BigIntegerField()
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='items', related_query_name='items')

    def __str__(self) -> str:
        return self.title

    @property
    def get_first_image_url(self):
        return f'{self.images.all().first().image.url}'

    @property
    def get_all_images_url(self):
        return [image_url.image.url for image_url in self.images.all()]

    def add_to_cart_url(self):
        return f'/store/{self.slug}/add-to-cart/'

    def remove_from_cart_url(self):
        return f'/store/{self.slug}/remove-from-cart/'

    def reduce_items_in_cart_url(self):
        return f'/store/{self.slug}/reduce-items-in-cart/'


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE,
                             related_name='images', related_query_name='images')
    image = models.FileField(upload_to=save_item_image_file_path)

    def __str__(self) -> str:
        return f'image for item {self.item.id}'

    def count(self):
        qs = ItemImage.objects.filter(item=self.item)
        for i in range(qs.count()):
            if qs[i] == self:
                return i


class OrderItem(models.Model):
    # id = RandomCharField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,
                              null=True, related_name='buyer', related_query_name='buyer')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField(null=True, blank=True)

    def __add__(self, x):
        if isinstance(x, OrderItem):
            return self.total_price + x.total_price

    def __radd__(self, x):
        if isinstance(x, int):
            return self.total_price + x

    def __str__(self) -> str:
        return f'{self.item.id} - {self.item.title}'

    def save(self, *args, **kwargs):
        self.total_price = self.item.price * self.quantity
        self.buyer = self.user
        return super().save(*args, **kwargs)  # Call the real save() method

    def in_user_cart(self):
        try:
            order = Order.objects.get(user=self.user, ordered=False)
            print(order)
            if order.items.filter(item__slug=self.item.slug).exists():
                return True
        except:
            return False


class Order(models.Model):
    id = RandomCharField(length=12, unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    total_price = models.IntegerField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Order - {self.id}'

    def total_items(self):
        total = 0
        for item in self.items.all():
            total += item.quantity
        return total

    def save(self, *args, **kwargs):
        self.total_price = sum(self.items.all())
        return super().save(*args, **kwargs)  # Call the real save() method


class BillingAddress(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.TextField()
    phone = models.CharField(max_length=11)
    payment_method = models.CharField(max_length=255, choices=PAYMENT_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, default=None, null=True)


class ShopItemReview(TimeStampedModel):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE,
                             related_name='reviews', related_query_name='reviews')
    subject = models.CharField(max_length=255)
    review = models.TextField()
    stars = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created']
        get_latest_by = 'created'


class SalesChat(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='item_chat_seller',
                               related_query_name='item_chat_seller', blank=True, null=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='item_chat_buyer', related_query_name='item_chat_buyer')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    modified = ModificationDateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-modified']

    def save(self, *args, **kwargs) -> None:
        self.seller = self.item.seller
        return super().save(*args, **kwargs)


class SalesChatMessage(models.Model):
    created = CreationDateTimeField()
    message = models.TextField()
    thread = models.ForeignKey(
        SalesChat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender', related_query_name='sender')
    reciever = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reciever', related_query_name='reciever')


class Sale(models.Model):
    id = RandomCharField(unique=True, primary_key=True,
                         length=16, uppercase=True)
    created = CreationDateTimeField()
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, blank=True,
                             null=True, related_name='sales', related_query_name='sales')
    buyer = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    price = models.PositiveIntegerField(default=0)
    payment_confirmed = models.BooleanField(default=False)
    used = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.PositiveBigIntegerField(blank=True, null=True)

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs) -> None:
        self.total_price = self.price * self.quantity
        return super().save(*args, **kwargs)
