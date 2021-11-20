from django.db import models


PRODUCT_CATEGORY = [
    ("A", "A"),
    ("B", "B"),
]


class Material(models.Model):

    material_name = models.CharField(max_length=255)
    amount = models.FloatField()
    measure_unit = models.CharField(max_length=255)


class Product(models.Model):

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    amount = models.FloatField()
    measure_unit = models.CharField(max_length=255)
    category = models.CharField(choices=PRODUCT_CATEGORY, max_length=255)
    price = models.FloatField()
    materials = models.ManyToManyField(Material, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Products"
        ordering = ['-created_at']
