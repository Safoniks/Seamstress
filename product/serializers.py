from django.shortcuts import get_object_or_404

from rest_framework import serializers

from .models import Product, ProductPhoto


class ProductPhotoListSerializer(serializers.Serializer):
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
    class Meta:
        model = ProductPhoto
        fields = (
            'id',
            'photo',
        )


class ProductListSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="product:product-detail", lookup_url_kwarg='product_id')
    # photos = serializers.SerializerMethodField()
    photos = ProductPhotoSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            # 'url',
            'id',
            'name',
            'description',
            'photos',
        )

    # def get_photos(self, obj):
    #     return ProductPhotoSerializer(obj.photos, many=True).data
