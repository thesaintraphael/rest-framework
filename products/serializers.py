from re import S
from rest_framework import serializers

from .models import Product, Material
from .utils import pop_materials


class MaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Material
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):

    add_materials = serializers.BooleanField(write_only=True)
    materials = MaterialSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = "__all__"
        extra_kwargs = {
            "owner": {"read_only": True}
        }

    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['materials'] = MaterialSerializer(instance.materials, many=True).data
        return representation

    def validate(self, attrs):

        if attrs['add_materials'] and not attrs['materials']:
            raise serializers.ValidationError(
                {"error": "Materials should be added, if add_materials is set to True"})

        attrs['owner'] = self.context['request'].user

        return attrs

    def create(self, validated_data):

        materials = pop_materials(validated_data)

        product = Product.objects.create(**validated_data)
        product.materials.set(materials)

        return product

    def update(self, instance, validated_data):
        materials = pop_materials(validated_data)
        
        product = super().update(instance, validated_data)
        product.materials.set(materials)

        return product
