from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('list', views.ProductsList.as_view(), name='product-list'),
    path('create', views.ProductCreate.as_view(), name='product-create')
]
