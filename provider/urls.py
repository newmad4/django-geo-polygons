from django.urls import path, register_converter
from rest_framework.routers import SimpleRouter

from provider.utils import LatConverter, LngConverter
from provider.views import PolygonAPIView, ProviderViewSet, ServiceAreaViewSet

register_converter(LatConverter, "lat")
register_converter(LngConverter, "lng")

app_name = "provider"
router = SimpleRouter(trailing_slash=False)

router.register("providers", ProviderViewSet, basename="providers")
router.register("services-ares", ServiceAreaViewSet, basename="services-ares")

api_url_patterns = [
    path("polygons/<lat:lat>/<lng:lng>", PolygonAPIView.as_view(), name="polygons"),
]

urlpatterns = router.urls + api_url_patterns
