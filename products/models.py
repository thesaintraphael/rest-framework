from django.db import models

from accounts.models import User


PRODUCT_CATEGORY = [
    ("A", "A"),
    ("B", "B"),
]


class Material(models.Model):

    material_name = models.CharField(max_length=255)
    amount = models.FloatField()
    measure_unit = models.CharField(max_length=255)


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    amount = models.FloatField()
    measure_unit = models.CharField(max_length=255)
    category = models.CharField(choices=PRODUCT_CATEGORY, max_length=255)
    price = models.FloatField()
    image = models.ImageField(upload_to="photos", blank=True, null=True)
    materials = models.ManyToManyField(Material, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Products"
        ordering = ['-created_at']
