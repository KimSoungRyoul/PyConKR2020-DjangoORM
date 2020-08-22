from random import randint

from django.contrib.auth.hashers import make_password
from orm_practice_app.models import User
from django.core.management import BaseCommand
from django.utils import timezone

from orm_practice_app.models import Company, Order, OrderedProduct, Product, UserInfo


class Command(BaseCommand):

    def handle(self, *args, **options):
        user_cnt = 100
        company_cnt = 100
        product_cnt = 100
        order_cnt = 1000

        suffix = User.objects.last().id if User.objects.exists() else 0

        for i in range(0, user_cnt, 20):
            User.objects.bulk_create([
                User(
                    username='username' + str(suffix + idx + i),
                    email='soungryoul.kim@deliveryhero.co.kr' + str(idx + i),
                    password=make_password('django_password'),
                    is_active=True,
                    userinfo=UserInfo.objects.create(tel_num=f"010-2222-34{i}"),
                ) for idx in range(1, 21)
            ])

        users = User.objects.all()

        for i in range(0, company_cnt, 20):
            Company.objects.bulk_create([
                Company(
                    name='company_name' + str(i + idx),
                    tel_num='070-123-4567',
                    address='서초구 ~~ 마제스타시티',
                ) for idx in range(1, 21)
            ])
        companies = Company.objects.all()

        for i in range(0, product_cnt, 100):
            Product.objects.bulk_create([
                Product(
                    name='product_name' + str(i + idx),
                    price=randint(10000, 100001),
                    product_owned_company=companies[randint(0, company_cnt - 1) // 2],
                ) for idx in range(1, 101)
            ])
        products = Product.objects.all()

        for i in range(0, order_cnt, 99):
            orders = Order.objects.bulk_create([
                Order(
                    descriptions='주문의 상세내용입니다...' + str(i + idx),
                    reg_date=timezone.now(),
                    order_owner=users[randint(0, user_cnt - 1) // 2],
                ) for idx in range(1, 101)
            ])

            OrderedProduct.objects.bulk_create([
                OrderedProduct(
                    product_cnt=randint(1, 30),
                    amount_of_credited_mileage=randint(100, 4000),
                    related_order=Order.objects.get(id=idx),
                    related_product=products[randint(0, product_cnt - 1) // 2],
                ) for idx in range(1, 100)
            ])

        self.stdout.write(self.style.SUCCESS('적당히 더미데이터 만들어짐....'))
