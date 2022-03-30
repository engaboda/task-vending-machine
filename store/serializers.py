from rest_framework import serializers
from .models import Product


class ProductRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Product


class ProductCreateSerializer(serializers.ModelSerializer):
    seller = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        fields = '__all__'
        model = Product


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Product


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('seller', )
        model = Product


class ProductBuySerializer(serializers.Serializer):
    productId = serializers.CharField()
    amount_of_product = serializers.IntegerField()


class ProductsBuySerializer(serializers.Serializer):
    product_info = ProductBuySerializer(many=True)
