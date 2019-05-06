from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, Count, Avg


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
    order_owner: User = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=False)
    product_set_included_order: set = models.ManyToManyField(to=Product, related_name='ordered_product_set',
                                                             through='OrderedProduct',
                                                             through_fields=('related_order', 'related_product'),
                                                             )


class UserAddress(models.Model):
    city = models.CharField(help_text='서울시,안양시,...', max_length=128, null=False)
    gu = models.CharField(help_text='서초구, 강남구,...,', max_length=128, null=False, default='')
    detail = models.CharField(help_text='104동 101호', max_length=128, null=False, default='')


class Mileage(models.Model):
    owned_userinfo = models.ForeignKey(to='UserInfo', on_delete=models.CASCADE, null=True)
    related_order = models.OneToOneField(Order, on_delete=models.CASCADE, null=False)
    amount = models.PositiveSmallIntegerField(default=0)
    descriptions = models.CharField(max_length=128, null=True)


class UserInfo(models.Model):
    owned_user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    tel_num = models.CharField(max_length=128, null=True)

#
# Order.objects.get(id=3).product_set_included_order.annotate(num_name_blabla=Count('name')).aggregate(Avg('num_name_blabla'))
