from django.urls import path, include
from rest_framework import routers
from .views import HistoricalTopTechnologiesViewSet, TechnologicalCountViewSet

router = routers.DefaultRouter()

# Register each viewset with the router
router.register(r'historical_stats', HistoricalTopTechnologiesViewSet)
router.register(r'usage_stats', TechnologicalCountViewSet)

# Main URL pattern that includes all routes URL
urlpatterns = [path('', include(router.urls))]
