from rest_framework import serializers

from .models import Product

class GetProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = [
            'p_author'
        ]

class PostProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = [
            'p_author'
        ]

class PutProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = [
            'p_author'
        ]