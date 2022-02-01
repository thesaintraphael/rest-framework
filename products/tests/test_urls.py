from django.test import SimpleTestCase
from django.urls import reverse, resolve

from ..views import ProductCreate, ProductDetail, ProductsList


PRODUCT_LIST_URL = reverse("products:product-list")
PRODUCT_DETAIL_URL = reverse("products:product-detail", kwargs={"id": 1})
PRODUCT_CREATE_URL = reverse("products:product-create")


class ProductTestCase(SimpleTestCase):
    
    def test_url_view_connection(self):
        self.assertEqual(resolve(PRODUCT_LIST_URL).func.view_class, ProductsList)
        self.assertEqual(resolve(PRODUCT_DETAIL_URL).func.view_class, ProductDetail)
        self.assertEqual(resolve(PRODUCT_CREATE_URL).func.view_class, ProductCreate)

