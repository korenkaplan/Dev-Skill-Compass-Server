from rest_framework import serializers
from .models import Technology, Role, Category


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    model = Category
    fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    model = Role
    fields = '__all__'
