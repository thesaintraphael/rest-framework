from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('list', views.ProductsList.as_view(), name='product-list'),
    path('<int:id>', views.ProductDetail.as_view(), name='product-detail'),
    path('create', views.ProductCreate.as_view(), name='product-create')
]
