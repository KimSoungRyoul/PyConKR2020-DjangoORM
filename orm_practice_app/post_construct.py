from random import randint

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from orm_practice_app.models import Company, Product, Order, OrderedProduct

for i in range(1, 1001):
    User.objects.bulk_create([
        User(
            username='username' + str(idx * i),
            email='soungryoul.kim@deliveryhero.co.kr',
            password=make_password('django_password'),
            is_active=True,
        ) for idx in range(1, 31)
    ])

for i in range(1, 101):
    Company.objects.bulk_create([
        Company(
            name='company_name' + str(idx),
            tel_num='070-123-4567',
            address='서초구 ~~ 마제스타시티',
        ) for idx in range(1, 51)
    ])

for i in range(1, 10001):
    Product.objects.bulk_create([
        Product(
            name='product_name' + str(idx * i),
            price=randint(10000, 100001),
            product_owned_company__id=randint(0, 5000),
        ) for idx in range(1, 11)
    ])

for i in range(1, 10001):
    order = Order.objects.bulk_create([
        Order(
            descriptions='주문의 상세내용입니다...' + str(idx * i),
            order_owner__id=randint(1, 50000),
        ) for idx in range(1, 11)
    ])

    OrderedProduct.objects.bulk_create([
        OrderedProduct(
            product_cnt=randint(1, 30),
            amount_of_credited_mileage=randint(100, 4000),
            related_order=order,
            related_product_id=randint(1, 100000)
        )
    ])
