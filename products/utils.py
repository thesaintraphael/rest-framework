from . import serializers


class SerializerUtil:

    def __init__(self, serializer_class) -> None:
        self.serializer_class = serializer_class

    def save_serializer(self, data, instance=None, context=None, **kwargs):

        serializer = self.serializer_class(
            instance=instance, data=data, context=context, **kwargs)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return serializer


def validate_materials(data, materials):

    add_materials = data.pop('add_materials')

    if add_materials:
        serializer = serializers.MaterialSerializer(data=materials, many=True)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    return []
