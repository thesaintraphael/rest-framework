from . import serializers


class SerializerUtil:

    def __init__(self, serializer_class) -> None:
        self.serializer_class = serializer_class

    @staticmethod
    def validate_password(password: str) -> None:
        first_isalpha = password[0].isalpha()
        if all(first_isalpha == character.isalpha() for character in password):
            raise serializers.ValidationError(
                {"error": "Password must be consist of at least one digit and letters"}
            )

    @staticmethod
    def get_request_from_context(context):
        return context.get('request')

    @staticmethod
    def required(value, field: str = None) -> None:
        """field is string representation of field name. Used to return error_message with key value"""

        error_message = "This field is required"

        if not value:
            if field:
                error_message = {f"{field}": error_message}

            raise serializers.ValidationError(error_message)

    def save_serializer(self, data, instance=None, context=None, **kwargs):

        serializer = self.serializer_class(
            instance=instance, data=data, context=context, **kwargs)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return serializer


def validate_materials(data, materials):

    add_materials = data.pop('add_materials')

    if add_materials:
        serializer = serializers.MaterialSerializer(
            data=materials, many=True)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    return []
