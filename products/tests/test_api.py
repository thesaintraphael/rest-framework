import tempfile
from PIL import Image

from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from .test_urls import PRODUCT_CREATE_URL
from .utils import remove_upladed_files


TEST_DIR = "tests/media/"


class ProductApiTestCase(TestCase):

    def setUp(self) -> None:

        self.user = get_user_model().objects.create(
            username="admin", email="admin@gmail.com"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_create_product(self):

        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)

            data = {
                "name": "Mobile",
                "amount": 5.6,
                "measure_unit": "kq",
                "category": "A",
                "price": 10,
                "image": ntf,
                "add_materials": False,
            }

            res = self.client.post(
                PRODUCT_CREATE_URL, data=data, format="multipart")
            self.assertEqual(res.status_code, 201)

    def tearDown(self) -> None:
        remove_upladed_files(TEST_DIR)
