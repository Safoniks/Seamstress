from rest_framework import serializers

from operation.serializers import ProductOperationListSerializer, ProductOperationListUpdateSerializer
from operation.models import Operation

from .models import Product, ProductPhoto


class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = (
            'id',
            'photo',
            'active',
        )
        extra_kwargs = {'active': {'read_only': True}}


class ProductPhotosCreateSerializer(serializers.Serializer):
    photos = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True
    )

    def create(self, validated_data):
        photo = None
        photos = []
        context = self.context
        product = context.get('product')
        images = validated_data.pop('photos')

        for img in images:
            photo = ProductPhoto.objects.create(
                photo=img,
                product=product,
                active=False,
                **validated_data
            )
            photos.append(photo)

        serialized_photos = ProductPhotoSerializer(photos, many=True).data
        context['photos'] = serialized_photos
        return photo


class ProductPhotosUpdateSerializer(serializers.Serializer):
    photos = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=ProductPhoto.objects.all()),
        write_only=True,
        default=[],
        required=False,
        allow_empty=True,
        allow_null=True
    )

    def get_fields(self, *args, **kwargs):
        fields = super(ProductPhotosUpdateSerializer, self).get_fields()
        product = self.context.get('product')
        all_photos = fields['photos'].child.queryset
        fields['photos'].child.queryset = all_photos.filter(product=product)
        return fields

    def update(self, instance, validated_data):
        context = self.context
        product = context.get('product')
        all_photos = product.all_photos
        old_photos = instance
        new_photos = validated_data.get('photos')

        for photo in new_photos:
            not photo.active and photo.activate()  # new photo added
        for photo in all_photos:
            photo not in new_photos and photo.delete()  # old photo removed

        serialized_photos = ProductPhotoSerializer(new_photos, many=True).data
        context['photos'] = serialized_photos
        return new_photos


class ProductOperationsCreateUpdateSerializer(serializers.Serializer):
    operations = ProductOperationListUpdateSerializer(
        many=True,
        write_only=True,
        default=[],
        required=False,
        allow_empty=True,
        allow_null=True
    )

    def validate_operations(self, value):
        if value:
            unique_operation_types = {operation.get('operation_type') for operation in value}
            if not len(unique_operation_types) == len(value):
                raise serializers.ValidationError('Must be an different operation types.')
        return value

    def create(self, validated_data):
        new_operation = None
        operation_list = []
        context = self.context
        product = context.get('product')
        operations = validated_data.pop('operations')

        for operation in operations:
            new_operation = Operation.objects.create(
                operation_type=operation.get('operation_type'),
                product=product,
                **validated_data
            )
            operation_list.append(new_operation)

        serialized_operations = ProductOperationListSerializer(operation_list, many=True).data
        context['operations'] = serialized_operations
        return new_operation

    def update(self, instance, validated_data):
        context = self.context
        product = context.get('product')
        old_operations = instance
        new_operations = validated_data.get('operations')
        new_operation_types = [operation['operation_type'] for operation in new_operations]

        for old_operation in old_operations:
            if old_operation.operation_type not in new_operation_types:
                old_operation.delete()  # old operation removed
            else:
                new_operation_types.remove(old_operation.operation_type)

        for new_operation_type in new_operation_types:
            operation = Operation(
                product=product,
                operation_type=new_operation_type
            )
            operation.save()  # new operation added

        new_operations = product.operations
        serialized_operations = ProductOperationListSerializer(new_operations, many=True).data
        context['operations'] = serialized_operations
        return new_operations


class ProductSerializer(serializers.ModelSerializer):
    photos = ProductPhotoSerializer(many=True, read_only=True)
    operations = ProductOperationListSerializer(many=True, read_only=True)
    description = serializers.CharField(default='', required=False, allow_blank=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'photos',
            'operations',
        )
