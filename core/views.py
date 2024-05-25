from rest_framework import generics
from .models import Technologies, Roles, Categories
from .serializers import TechnologySerializer, CategorySerializer, RoleSerializer


class TechnologiesListCreate(generics.ListCreateAPIView):
    queryset = Technologies.objects.all()
    serializer_class = TechnologySerializer


class TechnologiesRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Technologies.objects.all()
    serializer_class = TechnologySerializer


class CategoriesListCreate(generics.ListCreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer


class CategoriesRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer


class RolesListCreate(generics.ListCreateAPIView):
    queryset = Roles.objects.all()
    serializer_class = RoleSerializer


class RolesRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Roles.objects.all()
    serializer_class = RoleSerializer


# class TechnologyViewSet(viewsets.ModelViewSet):
#     queryset = Technologies.objects.all()
#     serializer_class = TechnologySerializer
#
#
# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Categories.objects.all()
#     serializer_class = CategorySerializer
#
#
# class RoleViewSet(viewsets.ModelViewSet):
#     queryset = Roles.objects.all()
#     serializer_class = RoleSerializer
