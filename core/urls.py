from django.urls import path, include
from rest_framework import routers
from .views import (TechnologyViewSet, CategoryViewSet, RoleViewSet)

router = routers.DefaultRouter()

# Register each viewset with the router
router.register(r'technologies', TechnologyViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'roles', RoleViewSet)

# Main URL pattern the includes all router URLS's
urlpatterns = [path('', include(router.urls))]
