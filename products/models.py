import os

from django.db import models
from django.dispatch import receiver

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


@receiver(models.signals.post_delete, sender=Product)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(models.signals.pre_save, sender=Product)
def auto_delete_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_image = Product.objects.get(pk=instance.pk).image
    except Product.DoesNotExist:
        return False

    new_image = instance.image
    if not old_image == new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)
