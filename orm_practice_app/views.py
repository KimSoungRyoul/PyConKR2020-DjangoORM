import json
from typing import List, Dict, Any, Type

from django.core.handlers.wsgi import WSGIRequest
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import QuerySet, Q
from django.forms import model_to_dict
from django.http import HttpResponse, QueryDict
from django.core.serializers import serialize

from orm_practice_app.models import User, Order, Company, Product


def i_am_function_view(request: WSGIRequest):
    # HTTP Request 잡아서 처리하는 로직
    query_params: QueryDict = request.POST

    # User를 선언하는 시점에 users는 다만 쿼리셋에 지나지 않았다.
    users: QuerySet = User.objects.all()
    if isinstance(users, QuerySet):
        print("users 는 아직 쿼리셋이기때문에 이 print문이 출력됩니다.")

    # list()로 쿼리셋을 불렀을때 users는 List[Model]이 된다.
    user_list: List[User] = list(users)  # 리스트로 묶는 시점에 실제 SQL이 호출됩니다.
    if isinstance(user_list, QuerySet):
        print("user_list는 쿼리셋이 아닙니다. 이 print문은 출력안됨")

    # 직렬화 로직
    user_list_dict: List[Dict[str, Any]] = [
        model_to_dict(user, fields=('id', 'username', 'is_staff', 'first_name', 'last_name', 'email'))
        for user in user_list
    ]
    # Dict로 직렬화한 데이터를 json 포맷을 가진 문자열로 풀어준다.
    user_list_json_array: str = json.dumps(user_list_dict, indent=1, cls=DjangoJSONEncoder)

    # 이 문자열을 httpResponse body(content)에 담아서 반환한다.
    return HttpResponse(content=user_list_json_array, content_type="application/json")


def i_am_function_view2(request: WSGIRequest):

    print('i_am_function_view2 호출.....')
    # User를 선언하는 시점에는 SQL이 호출되지 않음
    users: QuerySet = User.objects.all()

    # 아래 쿼리셋들을 선언만 해놓고 사용하지 않음 , 이러면 SQL이 호출되지 않는다.
    orders: QuerySet  = Order.objects.all()
    companies: QuerySet = Company.objects.all()


    print('')
    user_list: List[User] = list(users)

    # 직렬화 로직
    user_list_dict: List[Dict[str, Any]] = [
        model_to_dict(user, fields=('id', 'username', 'is_staff', 'first_name', 'last_name', 'email'))
        for user in user_list
    ]
    user_list_json_array: str = json.dumps(user_list_dict, indent=1, cls=DjangoJSONEncoder)

    return HttpResponse(content=user_list_json_array, content_type="application/json")




def i_am_function_view3(request: WSGIRequest):

    # User를 선언하는 시점에는 SQL이 호출되지 않음
    users: QuerySet = User.objects.all()

    # 0번째 User를 얻어오고싶어서 users쿼리셋은 SQL을 호출
    first_user: User = users[0]

    # 바로 윗줄에서 user1명밖에 가져오지 않아서 모든 user를 얻으려면 어쩔수 없이 다시 SQL을 호출해야함
    user_list: List[User] = list(users)


    # 직렬화 로직
    user_list_dict: List[Dict[str, Any]] = [
        model_to_dict(user, fields=('id', 'username', 'is_staff', 'first_name', 'last_name', 'email'))
        for user in user_list
    ]
    user_list_json_array: str = json.dumps(user_list_dict, indent=1, cls=DjangoJSONEncoder)

    return HttpResponse(content=user_list_json_array, content_type="application/json")



# N+1 Problem 예제
def i_am_function_view3_1(request: WSGIRequest):

    # User를 선언하는 시점에는 SQL이 호출되지 않음
    users: QuerySet = User.objects.all()

    # 개발자 관점에는 각user의 모든 userinfo가 필요한 것을 알지만 QuerySet은 그걸 모른다.
    for user in users:
        # QuerySet입장에서 user의 userinfo 가 필요한 시점은 여기다.
        # 따라서 userinfo를 알기위해 SQL을 for문이 돌때마다(N번) 호출한다.
        user.userinfo

    user_list: List[User] = list(users)

    # 직렬화 로직
    user_list_dict: List[Dict[str, Any]] = [
        model_to_dict(user)
        for user in user_list
    ]
    user_list_json_array: str = json.dumps(user_list_dict, indent=1, cls=DjangoJSONEncoder)

    return HttpResponse(content=user_list_json_array, content_type="application/json")



def i_am_function_view4(request: WSGIRequest):

    # User를 선언하는 시점에는 SQL이 호출되지 않음
    users: QuerySet = User.objects.all()


    user_list: List[User] = list(users)
    # 바로 위에서 users쿼리셋은 모든 user를 가져오는 SQL을 이미 호출함 따라서 0번째 user는 users쿼리셋에 캐싱된 값을 재활용함 (SQL호출 X)
    first_user: User = users[0]

    # 이 예제를 통해 배울점: 쿼리셋을 호출하는 순서가 바뀌는 것만으로도 QuerySet캐싱때문에 발생하는 SQL이 달라질수있다.


    # 직렬화 로직
    user_list_dict: List[Dict[str, Any]] = [
        model_to_dict(user, fields=('id', 'username', 'is_staff', 'first_name', 'last_name', 'email'))
        for user in user_list
    ]
    user_list_json_array: str = json.dumps(user_list_dict, indent=1, cls=DjangoJSONEncoder)

    return HttpResponse(content=user_list_json_array, content_type="application/json")


def i_am_function_view5(request: WSGIRequest):

    # company pk가 20아하인 Product들을 전부 조회
    company_queryset: QuerySet = Company.objects.filter(id__lte=20).values_list("id",flat=True)

    product_queryset: QuerySet =Product.objects.filter(product_owned_company__id__in=company_queryset)

    product_list: List[Product] = list(product_queryset)
    print(product_list)

    normal_joined_queryset = Order.objects.filter(descriptions__isnull=False, product_set_included_order__name="asdfsdf")

    subquery_executed_queryset = Order.objects.filter(descriptions__isnull=False).exclude(product_set_included_order__name="asdfsdf")

    subquery_executed_queryset2= Order.objects.filter(Q(descriptions__isnull=False), ~Q(product_set_included_order__name="asdfsdf"))

    normal_joined_queryset2 = Order.objects.filter(Q(descriptions__isnull=False)).exclude(order_owner__userinfo__tel_num="010-2222-342")

    list(normal_joined_queryset)
    list(subquery_executed_queryset)
    list(subquery_executed_queryset2)
    list(normal_joined_queryset2)
    return HttpResponse(content="", content_type="application/json")
