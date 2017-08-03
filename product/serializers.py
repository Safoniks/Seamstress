from rest_framework import serializers

from .models import Product, ProductPhoto


class ProductPhotosCreateSerializer(serializers.Serializer):
    photo = serializers.ListField(
        child=serializers.ImageField()
    )
    product_id = serializers.IntegerField()

    def validate(self, attrs):
        product_id = attrs.pop('product_id')
        try:
            product = Product.objects.get(id=product_id)
            attrs.update({'product': product})
        except:
            raise serializers.ValidationError('This product does not exist.')
        return attrs

    def create(self, validated_data):
        photo = None
        photos = validated_data.pop('photo')
        product = validated_data.pop('product')
        for img in photos:
            photo = ProductPhoto.objects.create(
                photo=img,
                product=product,
                **validated_data
            )
        return photo


class ProductPhotoSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="product:product-photo-detail", lookup_url_kwarg='photo_id')

    class Meta:
        model = ProductPhoto
        fields = (
            # 'url',
            'id',
            'photo',
        )


class ProductSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="product:product-detail", lookup_url_kwarg='product_id')
    photos = ProductPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            # 'url',
            'id',
            'name',
            'description',
            'photos',
        )
