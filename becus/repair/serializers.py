from rest_framework import serializers
from .models import Repair


# orders list serializer
class GetRepairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repair
        fields = '__all__'

class PostRepairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repair
        exclude = [
            'r_product',
            'r_status',
            'r_author'
        ]

class PutRepairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repair
        exclude = [
            'r_product',
            'r_status',
            'r_author'
        ]