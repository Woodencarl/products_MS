from rest_framework import serializers
from catalog.models import Products, Offers


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offers
        fields = "__all__"


class ProductOfferSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    offers = serializers.CharField()


