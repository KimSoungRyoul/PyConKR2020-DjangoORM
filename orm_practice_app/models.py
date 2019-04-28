from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    name: str = models.CharField(max_length=128, null=False)
    tel_num: str = models.CharField(max_length=128, null=True)
    address: str = models.CharField(max_length=128, null=False)


class Product(models.Model):
    name: str = models.CharField(null=False, max_length=128)
    price: int = models.PositiveIntegerField(null=False, default=0)
    product_owned_company: Company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=False)


class OrderedProduct(models.Model):
    product_cnt: int = models.PositiveIntegerField(null=False, default=1)
    amount_of_credited_mileage: int = models.PositiveIntegerField(null=False)

    related_product: Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    related_order = models.ForeignKey('Order', on_delete=models.CASCADE)


class Order(models.Model):
    descriptions: str = models.CharField(null=False, default='비어있음..', max_length=128)
    reg_date: datetime = models.DateTimeField(auto_created=True)
    order_owner: User = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    product_set_included_order: set = models.ManyToManyField(to=Product, related_name='ordered_product_set',
                                                             through='OrderedProduct',
                                                             through_fields=('related_order', 'related_product'),
                                                             )

