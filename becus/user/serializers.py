from rest_framework import serializers
from .models import User

class GetUserSerializer(serializers.ModelField):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'name',
            'phone',
            'role',
            'approval'
        )