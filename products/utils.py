from . import serializers

def pop_materials(data):

    add_materials = data.pop('add_materials')
    materials = data.pop('materials')

    if add_materials:
        serializer = serializers.MaterialSerializer(data=materials, many=True)
        serializer.is_valid(raise_exception=True)
        return serializer.save()
        
    return []
