from rest_framework import serializers
from .models import Gconsult, Pconsult

class GetGlobalConsultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gconsult
        fields = '__all__'

class PostGlobalConsultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gconsult
        exclude = [
            'gc_created_at',
            'gc_status',
            'gc_author'
        ]

class PutGlobalConsultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gconsult
        exclude = [
            'gc_created_at',
            'gc_status',
            'gc_author'
        ]

class GetProductConsultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pconsult
        fields = '__all__'

class PostProductConsultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pconsult
        exclude = [
            'pc_product',
            'pc_created_at',
            'pc_status',
            'pc_author'
        ]

class PutProductConsultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pconsult
        exclude = [
            'pc_product',
            'pc_created_at',
            'pc_status',
            'pc_author'
        ]