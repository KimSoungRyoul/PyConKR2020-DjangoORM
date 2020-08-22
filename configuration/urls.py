from django.contrib import admin
from django.urls import path

from orm_practice_app import queryset_pratice, views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('bulk_create/', queryset_pratice.asdf),

    path('i-am-api/', views.i_am_function_view),
    path('i-am-api2/', views.i_am_function_view2),
    path('i-am-api3/', views.i_am_function_view3),
    path('i-am-api3-1/', views.i_am_function_view3_1),
    path('i-am-api4/', views.i_am_function_view4),
    path('i-am-api5/', views.i_am_function_view5),
]
