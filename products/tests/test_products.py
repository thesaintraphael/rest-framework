from django.test import SimpleTestCase


class ProductTestCase(SimpleTestCase):
    
    def test_simple_case(self):
        
        self.assertEqual(1, 1)
