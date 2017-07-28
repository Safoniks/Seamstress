from rest_framework import serializers

from .models import Product, ProductPhoto


class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = (
            'id',
            'photo',
        )


class ProductListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="product:product-detail", lookup_url_kwarg='product_id')
    photos = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = (
            'url',
            'id',
            'name',
            'description',
            'photos',
        )

    def get_photos(self, obj):
        return ProductPhotoSerializer(obj.photos, many=True).data


class ProductDetailSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'photos',
        )

    def get_photos(self, obj):
        return ProductPhotoSerializer(obj.photos, many=True).data

