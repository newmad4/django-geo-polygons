from typing import Any

from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from provider.models import Provider, ServiceArea
from provider.serializers import (
    ProviderDetailSerializer,
    ProviderListSerializer,
    ProviderSerializer,
    ServiceAreaDetailSerializer,
    ServiceAreaListSerializer,
    ServiceAreaSerializer
)
from provider.utils import get_services_areas_by_point

__all__ = [
    "ProviderViewSet",
    "ServiceAreaViewSet",
    "PolygonAPIView",
]


class ProviderViewSet(ModelViewSet):
    """CRUD API for work with Provider."""
    queryset = Provider.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ProviderListSerializer
        elif self.action == "retrieve":
            return ProviderDetailSerializer
        else:
            return ProviderSerializer

    def get_queryset(self) -> 'QuerySet[Provider]':
        if self.action == "list":
            return self.queryset.only("name", "email").order_by("name")
        elif self.action == "retrieve":
            return self.queryset.prefetch_related("services_areas")
        else:
            return self.queryset


class ServiceAreaViewSet(ModelViewSet):
    """CRUD API for work with Services Areas."""
    queryset = ServiceArea.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ServiceAreaListSerializer
        elif self.action == "retrieve":
            return ServiceAreaDetailSerializer
        else:
            return ServiceAreaSerializer

    def get_queryset(self) -> 'QuerySet[ServiceArea]':
        if self.action == "list":
            return self.queryset.only("name", "price").order_by("name")
        elif self.action == "retrieve":
            return self.queryset.select_related("provider")
        else:
            return self.queryset


class PolygonAPIView(APIView):

    @staticmethod
    def get(request: Request, lat: float, lng: float, *args: Any, **kwargs: Any) -> Response:
        """Endpoint which return list of all polygons with containing a point with
        chosen coordinates.

        We expect that coordinate system is "DD.DDDDD".
        """
        polygons_containing_point = get_services_areas_by_point(lat, lng)
        return Response(polygons_containing_point)
