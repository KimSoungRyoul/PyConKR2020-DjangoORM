from django.contrib.auth.models import User
from django.db.models import Subquery, F, Count, Avg
from django.db.models.functions import Substr
from django.db.models import prefetch_related_objects

from orm_practice_app.models import UserInfo, Product, Company

users = User.objects.filter(id__lte=30)

UserInfo.objects.filter(owned_user__in=Subquery(User.objects.filter(id__lte=30).values('id'))).explain()

"""
SELECT "orm_practice_app_userinfo"."id",
"orm_practice_app_userinfo"."owned_user_id",
 "orm_practice_app_userinfo"."tel_num" 
 
 FROM "orm_practice_app_userinfo" 
 
 WHERE "orm_practice_app_userinfo"."owned_user_id" 
        IN (SELECT U0."id" FROM "auth_user" U0 WHERE U0."id" <= 30)

"""

# EXPLAIN QUERY PLAN
"""

Execution time: 0.000090s [Database: default]

    '3 0 0 SEARCH TABLE orm_practice_app_userinfo USING INDEX orm_practice_app_userinfo_owned_user_id_e85907f1 (owned_user_id=?)
     7 0 0 LIST SUBQUERY 1
     9 7 0 SEARCH TABLE auth_user AS U0 USING INTEGER PRIMARY KEY (rowid<?)'

"""

User.objects.annotate(first=Substr("first_name", 1, 1), last=Substr("last_name", 1, 1)).filter(first=F("last"))

"""
SELECT "auth_user"."id",
     "auth_user"."password",
      "auth_user"."last_login",
       "auth_user"."is_superuser",
    "auth_user"."username",
     "auth_user"."first_name",
      "auth_user"."last_name",
       "auth_user"."email",
        "auth_user"."is_staff",
         "auth_user"."is_active",
         "auth_user"."date_joined", 
         SUBSTR("auth_user"."first_name", 1, 1) AS "first",
        SUBSTR("auth_user"."last_name", 1, 1) AS "last" 
         
         FROM "auth_user" 
         WHERE SUBSTR("auth_user"."first_name", 1, 1) = (SUBSTR("auth_user"."last_name", 1, 1))
"""

duplicates = User.objects.values('first_name').annotate(name_count=Count('first_name')).filter(name_count__gt=1)




Product.objects.aggregate(Avg('price'))

product_list = list(Product.objects.filter(id__lte=10))

execute_prefetch= True

if execute_prefetch:
    # 원하는 시점에 +1 쿼리 prefetch 쿼리를 실행할수 있다.
    prefetch_related_objects(product_list, 'product_owned_company')

    # 위에서 prefetch 쿼리가 실행되어서 n+1 problem이 발생하지 않는다.
    for product in product_list:
        print(product.product_owned_company)

else:
    # 여기서는 +1 쿼리가 발생안해서 n+1Problem 발생한다
    for product in product_list:
        print(product.product_owned_company)
