from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass

class Auctions(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="seller")
    title = models.CharField(max_length=100, default=None)
    product = models.URLField(max_length=600, default="https://png.pngtree.com/png-clipart/20190925/original/pngtree-no-image-vector-illustration-isolated-png-image_4979075.jpg")
    price = models.DecimalField(max_digits=200, decimal_places=2)
    description = models.TextField()
    is_closed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True)

categories = (
    ('Fashion', 'Fashion'),
    ('Electronics', 'Electronics'),
    ('Toys', 'Toys'),
    ('Men', 'Men'),
    ('Women', 'Women'),
    ('Children', 'Children'),
    ('Shoes', 'Shoes'),
    ('Furniture', 'Furniture'),
    ('Clothing', 'Clothing'),
    ('Hair', 'Hair'),
    ('Watches', 'Watches'),
)


class Category(models.Model):
    product_category = models.CharField(max_length=30, choices=categories, unique=True)
    auctio = models.ManyToManyField(Auctions, related_name="Auc_Cat")

    def __str__(self):
        return f"{self.product_category}"

class Bid(models.Model):
    item = models.ForeignKey(Auctions, on_delete=models.CASCADE, related_name="bidItem")
    buyer =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="buyer", default=None)
    bidPrice = models.DecimalField(max_digits=200, decimal_places=2)

class Comments(models.Model):
    listing = models.ForeignKey(Auctions, on_delete=models.CASCADE, related_name="auctionItem")
    comment = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="person")
    timestamp = models.DateTimeField(auto_now=True)

class Watch(models.Model):
    watch_product = models.ForeignKey(Auctions, on_delete=models.CASCADE, related_name="watchItem")
    watch_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="userWatch")


