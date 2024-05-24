from rest_framework import serializers
from .models import Technologies, Roles, Categories


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technologies
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'

