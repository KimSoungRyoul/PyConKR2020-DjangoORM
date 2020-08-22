from datetime import datetime

from django.contrib.auth.models import User, AbstractUser
from django.db import models

"""
사업자 1명은 상품(Product) N개를 가질수 있다
주문 1개는 상품(Product) 와 M:N 관계  (RelationTable=>OrderedProduct)
주문 1개는 그 주문으로 발생한 마일리지정보와 1대1관계다. 
"""


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
    related_order = models.ForeignKey('Order', on_delete=models.CASCADE, null=True)


class Order(models.Model):
    descriptions: str = models.CharField(null=False, default='비어있음..', max_length=128)
    reg_date: datetime = models.DateTimeField(auto_created=True)
    order_owner: User = models.ForeignKey(to='orm_practice_app.User', on_delete=models.CASCADE, null=True, blank=False)
    product_set_included_order: set = models.ManyToManyField(to=Product, related_name='ordered_product_set',
                                                             through='OrderedProduct',
                                                             through_fields=('related_order', 'related_product'),
                                                             )


class UserAddress(models.Model):
    user_info = models.ForeignKey(to="UserAddress", on_delete=models.CASCADE)

    city = models.CharField(help_text='서울시,안양시,...', max_length=128, null=False)
    gu = models.CharField(help_text='서초구, 강남구,...,', max_length=128, null=False, default='')
    detail = models.CharField(help_text='104동 101호', max_length=128, null=False, default='')


class Mileage(models.Model):
    owned_userinfo = models.ForeignKey(to='orm_practice_app.User', on_delete=models.CASCADE, null=True)
    related_order = models.OneToOneField(Order, on_delete=models.CASCADE, null=False)
    amount = models.PositiveSmallIntegerField(default=0)
    descriptions = models.CharField(max_length=128, null=True)


class UserInfo(models.Model):
    tel_num = models.CharField(max_length=128, null=True)


class User(AbstractUser):
    userinfo = models.OneToOneField('orm_practice_app.UserInfo', on_delete=models.CASCADE, null=False)
    aab = models.ForeignKey("AAB", on_delete=models.CASCADE, null=True)


class AAB(models.Model):
    name = models.CharField(max_length=32, default="dsfsdf")


#
# Order.objects.get(id=3).product_set_included_order.annotate(num_name_blabla=Count('name')).aggregate(Avg('num_name_blabla'))


class Asf(object):
    asdf = ''

#
# order_list = (
#     Order.objects
#     .select_related('order_owner')
#     .filter(order_owner__username='username4')
#     .prefetch_related('product_set_included_order')
# )
#
# mil_list = (
#     Mileage.objects.prefetch_related('owned_userinfo','related_order__product_set_included_order')
# )