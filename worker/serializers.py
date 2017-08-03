from rest_framework import serializers

# from .models import Product, ProductPhoto
#
#
# class ProductSerializer(serializers.ModelSerializer):
#     # url = serializers.HyperlinkedIdentityField(view_name="product:product-detail", lookup_url_kwarg='product_id')
#     photos = ProductPhotoSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Product
#         fields = (
#             # 'url',
#             'id',
#             'name',
#             'description',
#             'photos',
#         )
