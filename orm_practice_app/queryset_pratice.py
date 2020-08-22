from typing import List

from django.contrib.auth.models import User
from django.db.models import Q, FilteredRelation, F, Sum, Avg, Subquery, Prefetch, QuerySet

from orm_practice_app.models import Company, Product, Order, OrderedProduct


def asdf():
    Product.objects.filter(name='product_name3', product_owned_company__name='company_name20').select_related(
        'product_owned_company')

    Company.objects.prefetch_related('company_set').filter(product__name='product_anme8')

    Product.objects.filter(product_owned_company__name='company_name133')
    Order.objects.filter(order_owner__is_active=True)
    User.objects.filter(order__descriptions__contains='asdf')
    OrderedProduct.objects.filter(related_order__order_owner__user_permissions__isnull=True)
    OrderedProduct.objects.filter(product_cnt=30).prefetch_related('related_order')

    # product_set을 prefetched_related로 가져오는 쿼리셋 선언
    company_queryset: QuerySet = Company.objects.prefetch_related('product_set').filter(name='company_name1')
    # 쿼리셋을 수행하면 아래와 같은 쿼리 2개 발생 문제 없음
    comapny_list: List[Company]= list(company_queryset)
    """
    SELECT "orm_practice_app_company"."id", "orm_practice_app_company"."name", "orm_practice_app_company"."tel_num", "orm_practice_app_company"."address" 
        FROM "orm_practice_app_company" 
            WHERE "orm_practice_app_company"."name" = 'company_name1'  LIMIT 21;
    -- prefetch_related() 구절이 아래 SQL을 부른다 --       
    SELECT "orm_practice_app_product"."id", "orm_practice_app_product"."name", "orm_practice_app_product"."price", "orm_practice_app_product"."product_owned_company_id" 
        FROM "orm_practice_app_product" 
            WHERE "orm_practice_app_product"."product_owned_company_id" IN (1, 21);

    """
    # 위와같은 방식에는 문제가 없다
    # 하지만?
    company_queryset: QuerySet = Company.objects.prefetch_related(
        Prefetch('product_set', queryset=Product.objects.filter(product__name='product_name3'))).filter(
        name='company_name1')
    # 이렇게 product관련 조건절이 추가된다면 어떨까
    # 쿼리셋을 수행하면 아래와 같은 잘못된 쿼리가 발생한다.
    comapny_list: List[Company] = list(company_queryset)
    """
    SELECT "orm_practice_app_company"."id", "orm_practice_app_company"."name", "orm_practice_app_company"."tel_num", "orm_practice_app_company"."address" 
        FROM "orm_practice_app_company" 
            INNER JOIN "orm_practice_app_product" ON ("orm_practice_app_company"."id" = "orm_practice_app_product"."product_owned_company_id") 
        WHERE ("orm_practice_app_company"."name" = 'company_name1' AND "orm_practice_app_product"."name" = 'product_name3')  LIMIT 21;
    -- prefetch_related가 쿼리를 발생시켰지만 윗 쿼리에서 불필요한 조인이 발생한다. --
    SELECT "orm_practice_app_product"."id", "orm_practice_app_product"."name", "orm_practice_app_product"."price", "orm_practice_app_product"."product_owned_company_id" 
        FROM "orm_practice_app_product" 
    WHERE "orm_practice_app_product"."product_owned_company_id" IN (1);

    """
    # 이는 가장 흔히 발생할수 있는 문제다. 해당 쿼리셋을 수행했을때
    # 1.조인을 하던지
    # 2.추가쿼리에서 조건절이 붙던지
    # 둘중 하나만 수행되었어야 효율적인 쿼리다. 그러나 생각없이 prefetch_related를 붙이면 이런식으로 잘못된 쿼리가 수행될수있다






    # 1-2 이 쿼리는 prefetch_related를 사용했음에도 불구하고 QuerySet 평가시 추가적인 쿼리가 불필요하다 판단하여 inner join 전략을 택한다. 이경우는 .prefetch_related('related_order') 이 로직은 무시된다
    OrderedProduct.objects.filter(Q(product_cnt=30) & Q(related_order__descriptions='asdf')).prefetch_related('related_order')
    """
     SELECT * 
     FROM "orm_practice_app_orderedproduct" 
     INNER JOIN "orm_practice_app_order" ON ("orm_practice_app_orderedproduct"."related_order_id" = "orm_practice_app_order"."id") 
     WHERE ("orm_practice_app_orderedproduct"."product_cnt" = 30 AND "orm_practice_app_order"."descriptions" = 'asdf') 
    """

    # 1-3 이 쿼리는 의도한대로 +1개의 쿼리로 related_order를 조회한다 filter절에서 related_order에 대해 별다른 내용이 없어서 반항없이 개발자의 의도대로 따라준다.
    OrderedProduct.objects.filter(product_cnt=30).prefetch_related('related_order')
    """
    SELECT * 
    FROM "orm_practice_app_orderedproduct"
     WHERE "orm_practice_app_orderedproduct"."product_cnt" = 30  LIMIT 21;

    SELECT * 
     FROM "orm_practice_app_order" 
     WHERE "orm_practice_app_order"."id" IN (135, 776, 404, 535, 151, 280, 666, 155, 29, 675, 548, 298, 45, 48, 177, 306, 336, 729, 605, 226, 739);

    """

    # 이러면 prefetch_related()를 붙혀준 의도대로 +1 쿼리로 'related_order'를 조회한다 그러나 완벽히 의도한 쿼리가 생성되지 않는다.
    OrderedProduct.objects.filter(Q(product_cnt=30) | Q(related_order__descriptions='asdf')).prefetch_related('related_order')
    """
    SELECT *
        FROM "orm_practice_app_orderedproduct" 
        INNER JOIN "orm_practice_app_order" ON ("orm_practice_app_orderedproduct"."related_order_id" = "orm_practice_app_order"."id") 
        WHERE ("orm_practice_app_orderedproduct"."product_cnt" = 30 OR "orm_practice_app_order"."descriptions" = 'asdf');
        
    SELECT *
       FROM "orm_practice_app_order" 
       WHERE "orm_practice_app_order"."id" IN (135, 776, 404, 535, 151, 280, 666, 155, 29, 675, 548, 298, 45, 48, 177, 306, 336, 729, 605, 226, 739); 
    """
    # prefetch_related()로 추가되는 쿼리에 조건을 걸어주고 싶다면 Prefetch()를 사용해야한다
    OrderedProduct.objects.filter(Q(product_cnt=30)).prefetch_related(Prefetch('related_order', queryset=Order.objects.filter(descriptions='asdf')))
    """
     SELECT *
      FROM "orm_practice_app_orderedproduct" 
      WHERE "orm_practice_app_orderedproduct"."product_cnt" = 30 ;
      
     SELECT * 
      FROM "orm_practice_app_order" 
      WHERE ("orm_practice_app_order"."descriptions" = 'asdf' 
      AND "orm_practice_app_order"."id" IN (515, 644, 135, 391, 267, 526, 529, 660, 21, 663, 280, 422, 47, 707, 336, 593, 98, 228, 486, 374, 379));

    
    """

    # 앞 쿼리들의 결과에서도 봤듯이 OrderProduct->Order 참조에 관련된 쿼리는 정방향 참조이기때문에 충분히 inner join 전략을 택할수 있다
    # 그래서 앞에서 prefetch_related()를 붙이지 않거나 prefetch_related를 붙이더라도 +1 query를 만들지 않고 Django QuerySet은 최대한 inner join전략을 택하려고 노력한다.
    OrderedProduct.objects.filter(Q(product_cnt=30) & Q(related_order__descriptions='asdf')).select_related(
        'related_order')
    """
    SELECT * 
    FROM "orm_practice_app_orderedproduct"
     INNER JOIN "orm_practice_app_order" ON ("orm_practice_app_orderedproduct"."related_order_id" = "orm_practice_app_order"."id") 
     WHERE ("orm_practice_app_orderedproduct"."product_cnt" = 30 AND "orm_practice_app_order"."descriptions" = 'asdf') 
    
    """

    # 2-1 이러면 대참사가 발생한다.   foransdmf  이것을 N+1 Select Problem 이라고 한다.
    companys = Company.objects.filter(name__startswith='company_name')
    for company in companys:
        print(company.product_set[0])
    """
       SELECT * FROM "orm_practice_app_company" WHERE "orm_practice_app_company"."name"::text LIKE 'company\_name%';
           SELECT * FROM "orm_practice_app_product" WHERE "orm_practice_app_product"."product_owned_company_id" = 301;
           SELECT * FROM "orm_practice_app_product" WHERE "orm_practice_app_product"."product_owned_company_id" = 302;
           SELECT * FROM "orm_practice_app_product" WHERE "orm_practice_app_product"."product_owned_company_id" = 303;
           SELECT * FROM "orm_practice_app_product" WHERE "orm_practice_app_product"."product_owned_company_id" = 304;
           SELECT * FROM "orm_practice_app_product" WHERE "orm_practice_app_product"."product_owned_company_id" = 305;    
           SELECT * FROM "orm_practice_app_product" WHERE "orm_practice_app_product"."product_owned_company_id" = 306;   
    """

    # 2-2 이러면 딱 2개의 쿼리만 발생한다 prefetch_related를 가장 적절하게 활용한 좋은 예제이다.
    # prefetch_related()는 역참조해야 하는 상황에서 아래와 같은 N+1문제를 방지한다.
    # 단순 one table join과 같은 상황에서는 django orm이 최대한 inner join를 우선적으로 고민하고 불가능하면 left outer join로
    companys = Company.objects.filter(name__startswith='company_name').prefetch_related('product_set')
    for company in companys:
        print(company.product_set[0])

    # 3-1 product_owned_company필드에 null=True 옵션이 있다 이런경우는 outer join
    Product.objects.filter(price__gt=24000).select_related('product_owned_company')
    """
     SELECT * 
     FROM "orm_practice_app_product" 
     LEFT OUTER JOIN "orm_practice_app_company" ON ("orm_practice_app_product"."product_owned_company_id" = "orm_practice_app_company"."id")
      WHERE "orm_practice_app_product"."price" > 24000 
    """
    Product.objects.filter(price__gt=24000, product_owned_company__isnull=False).select_related('product_owned_company')
    Product.objects.filter(price__gt=24000, product_owned_company__isnull=False).select_related('product_owned_company')
    """
    SELECT * 
    FROM "orm_practice_app_product" 
    INNER JOIN "orm_practice_app_company" ON ("orm_practice_app_product"."product_owned_company_id" = "orm_practice_app_company"."id")
     WHERE ("orm_practice_app_product"."price" > 24000 AND "orm_practice_app_product"."product_owned_company_id" IS NOT NULL);  
    """

    # 4-1 Join Table에 제약 주기  FilteredRelation()는 Django2.0부터 가능
    Product.objects.select_related('this_is_join_table_name').annotate(this_is_join_table_name=FilteredRelation('product_owned_company',
                                                                      condition=Q(
                                                                          product_owned_company__name='company_name34'),),
                             ).filter(this_is_join_table_name__isnull=False)
    """
    SELECT "orm_practice_app_product"."id", "orm_practice_app_product"."name", "orm_practice_app_product"."price", "orm_practice_app_product"."product_owned_company_id" 
    FROM "orm_practice_app_product" 
    INNER JOIN "orm_practice_app_company" this_is_join_table_name
        ON ("orm_practice_app_product"."product_owned_company_id" =  this_is_join_table_name."id" AND ( this_is_join_table_name."name" = 'company_name34')
            ) 
    WHERE  this_is_join_table_name."id" IS NOT NULL ;

    
    """

    # 내가 원한다고 쿼리를 나눌수있는게 아니다.
    OrderedProduct.objects.filter(product_cnt=23000,
                                  related_product__product_owned_company__name__contains='comapny_name').prefetch_related(
        'related_product')
    """
     SELECT *
      FROM "orm_practice_app_orderedproduct" 
        INNER JOIN "orm_practice_app_product" ON ("orm_practice_app_orderedproduct"."related_product_id" = "orm_practice_app_product"."id")
        INNER JOIN "orm_practice_app_company" ON ("orm_practice_app_product"."product_owned_company_id" = "orm_practice_app_company"."id") 
      WHERE ("orm_practice_app_orderedproduct"."product_cnt" = 23000 AND "orm_practice_app_company"."name"::text LIKE '%comapny\_name%')
    
    """

    # 결론은 무거울 것으로 예상되는 QuerySet은 직접 쿼리는 찍어서 확인을 해야한다.
    OrderedProduct.objects.filter(product_cnt=23000,
                                  related_product__product_owned_company__name__contains='comapny_name').prefetch_related(
        'related_product', 'related_product__product_owned_company')

    """
    SELECT "orm_practice_app_orderedproduct"."id", "orm_practice_app_orderedproduct"."product_cnt", "orm_practice_app_orderedproduct"."amount_of_credited_mileage", "orm_practice_app_orderedproduct"."related_product_id", "orm_practice_app_orderedproduct"."related_order_id" 
    FROM "orm_practice_app_orderedproduct" 
        INNER JOIN "orm_practice_app_product" ON ("orm_practice_app_orderedproduct"."related_product_id" = "orm_practice_app_product"."id")
        INNER JOIN "orm_practice_app_company" ON ("orm_practice_app_product"."product_owned_company_id" = "orm_practice_app_company"."id") 
    WHERE ("orm_practice_app_orderedproduct"."product_cnt" = 23000 AND "orm_practice_app_company"."name"::text LIKE '%comapny\_name%') 
    """

    OrderedProduct.objects.filter(product_cnt=23000).prefetch_related(
        Prefetch('related_product__product_owned_company',
                 queryset=Company.objects.filter(name__contains='comapny_name')))
    """
    SELECT "orm_practice_app_orderedproduct"."id", "orm_practice_app_orderedproduct"."product_cnt",
       "orm_practice_app_orderedproduct"."amount_of_credited_mileage", "orm_practice_app_orderedproduct"."related_product_id",
       "orm_practice_app_orderedproduct"."related_order_id"
    FROM "orm_practice_app_orderedproduct" 
      INNER JOIN "orm_practice_app_product" ON ("orm_practice_app_orderedproduct"."related_product_id" = "orm_practice_app_product"."id")
      INNER JOIN "orm_practice_app_company" ON ("orm_practice_app_product"."product_owned_company_id" = "orm_practice_app_company"."id") 
    WHERE ("orm_practice_app_orderedproduct"."product_cnt" = 23000 AND "orm_practice_app_company"."name"::text LIKE '%comapny\_name%')
    """


    order_list: Order = Order.objects.filter(id=3).prefetch_related('product_set_included_order')
    """
    SELECT "orm_practice_app_order"."id", "orm_practice_app_order"."reg_date", "orm_practice_app_order"."descriptions", "orm_practice_app_order"."order_owner_id" 
    FROM "orm_practice_app_order" WHERE "orm_practice_app_order"."id" = 3  ;
    
    SELECT ("orm_practice_app_orderedproduct"."related_order_id") AS "_prefetch_related_val_related_order_id",
     "orm_practice_app_product"."id", "orm_practice_app_product"."name", "orm_practice_app_product"."price", "orm_practice_app_product"."product_owned_company_id" 
    FROM "orm_practice_app_product" 
        INNER JOIN "orm_practice_app_orderedproduct" ON ("orm_practice_app_product"."id" = "orm_practice_app_orderedproduct"."related_product_id") 
    WHERE "orm_practice_app_orderedproduct"."related_order_id" IN (3);
    """

    Order.objects.filter(id=4, product_set_included_order__product_owned_company=3)
    """
    SELECT "orm_practice_app_order"."id", "orm_practice_app_order"."reg_date", "orm_practice_app_order"."descriptions", "orm_practice_app_order"."order_owner_id" 
    FROM "orm_practice_app_order" 
        INNER JOIN "orm_practice_app_orderedproduct" ON ("orm_practice_app_order"."id" = "orm_practice_app_orderedproduct"."related_order_id") 
        INNER JOIN "orm_practice_app_product" ON ("orm_practice_app_orderedproduct"."related_product_id" = "orm_practice_app_product"."id") 
    WHERE ("orm_practice_app_order"."id" = 4 AND "orm_practice_app_product"."product_owned_company_id" = 3)
    """

    Order.objects.filter(id=4).prefetch_related('product_set_included_order')
    """
    SELECT * FROM "orm_practice_app_order" 
    WHERE "orm_practice_app_order"."id" = 4  LIMIT 21; 
    SELECT * FROM "orm_practice_app_product"
     INNER JOIN "orm_practice_app_orderedproduct" ON ("orm_practice_app_product"."id" = "orm_practice_app_orderedproduct"."related_product_id") 
     WHERE "orm_practice_app_orderedproduct"."related_order_id" IN (4); 

    """

    order_product = OrderedProduct.objects.filter(related_order=4).select_related('related_order', 'related_product')
    """
    SELECT "orm_practice_app_orderedproduct"."id", "orm_practice_app_orderedproduct"."product_cnt", 
    "orm_practice_app_orderedproduct"."amount_of_credited_mileage", "orm_practice_app_orderedproduct"."related_product_id", "orm_practice_app_orderedproduct"."related_order_id", 
    "orm_practice_app_product"."id", "orm_practice_app_product"."name", "orm_practice_app_product"."price", "orm_practice_app_product"."product_owned_company_id",
     "orm_practice_app_order"."id", "orm_practice_app_order"."reg_date", "orm_practice_app_order"."descriptions", "orm_practice_app_order"."order_owner_id" 
    FROM "orm_practice_app_orderedproduct" 
        INNER JOIN "orm_practice_app_order" ON ("orm_practice_app_orderedproduct"."related_order_id" = "orm_practice_app_order"."id") 
        INNER JOIN "orm_practice_app_product" ON ("orm_practice_app_orderedproduct"."related_product_id" = "orm_practice_app_product"."id") 
    WHERE "orm_practice_app_orderedproduct"."related_order_id" = 4 
    """

    order_queryset = Order.objects.filter(descriptions__contains='상세내용입니다').prefetch_related(
        'product_set_included_order')

    for order in order_queryset[:10]:
        order.product_set_included_order.all()

    """
    SELECT "orm_practice_app_order"."id", "orm_practice_app_order"."reg_date", "orm_practice_app_order"."descriptions", "orm_practice_app_order"."order_owner_id" 
    FROM "orm_practice_app_order" 
        INNER JOIN "orm_practice_app_orderedproduct" ON ("orm_practice_app_order"."id" = "orm_practice_app_orderedproduct"."related_order_id") 
    WHERE ("orm_practice_app_order"."id" = 4 AND "orm_practice_app_orderedproduct"."related_product_id" IS NOT NULL) ;

    
    """

    Product.objects.filter(id=4).select_related('product_owned_company')
    """
     SELECT "orm_practice_app_product"."id", "orm_practice_app_product"."name", "orm_practice_app_product"."price",
      "orm_practice_app_product"."product_owned_company_id", "orm_practice_app_company"."id", "orm_practice_app_company"."name",
       "orm_practice_app_company"."tel_num", "orm_practice_app_company"."address" 
     FROM "orm_practice_app_product" 
        LEFT OUTER JOIN "orm_practice_app_company" ON ("orm_practice_app_product"."product_owned_company_id" = "orm_practice_app_company"."id") 
     WHERE "orm_practice_app_product"."id" = 4;
    """

    Product.objects.annotate(custom_field=F('name') + F('price')).filter(id=3)

    # 일단 데이터를 다 가져와서 sum(product_set.value_list('price'))
    Product.objects.filter(id__lte=10).aggregate(total_price=Avg('price'))
    """
    SELECT AVG("orm_practice_app_product"."price") AS "total_price"
    FROM "orm_practice_app_product"
    WHERE "orm_practice_app_product"."id" <= 10

    """

    # 서브쿼리로 가져오기
    users = User.objects.filter(id__lte=20)
    Order.objects.filter(order_owner__in=Subquery(users.values('id')))
    """
     SELECT "orm_practice_app_order"."id", "orm_practice_app_order"."reg_date",
      "orm_practice_app_order"."descriptions", "orm_practice_app_order"."order_owner_id"
       FROM "orm_practice_app_order" 
       WHERE "orm_practice_app_order"."order_owner_id" IN (SELECT U0."id" FROM "auth_user" U0);
    """

    Order.objects.filter(order_owner_id__lte=20)


    # right outer 가능한가? 불가
    Product.objects.filter(product_owned_company__name='company_name3').select_related('product_owned_company')

    # many to many join
    Order.objects.prefetch_related('product_set_included_order').filter(id=1)


    aa=Order.objects.filter(descriptions__isnull=False,product_set_included_order__name="asdfsdf")

    bb= Order.objects.filter(Q(descriptions__isnull=False)).exclude(order_owner__userinfo__tel_num="010-2222-342")

