from rest_framework import serializers
from .models import Order


# orders list serializer
class GetOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class PostOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = [
            'o_product',
            'o_status',
            'o_author'
        ]

class PutOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = [
            'o_product',
            'o_status',
            'o_author'
        ]