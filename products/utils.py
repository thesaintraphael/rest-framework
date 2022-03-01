from . import serializers


def validate_materials(data, materials):

    add_materials = data.pop('add_materials')

    if add_materials:
        serializer = serializers.MaterialSerializer(data=materials, many=True)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    return []
