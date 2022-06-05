from rest_framework import serializers

from provider.models import Provider, ServiceArea

__all__ = [
    "ServiceAreaListSerializer",
    "ServiceAreaDetailSerializer",
    "ProviderListSerializer",
    "ProviderDetailSerializer",
    "PolygonSerializer",
    "ServiceAreaSerializer",
    "ProviderSerializer",
]


class ServiceAreaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceArea
        fields = ("id", "name", "price")


class ProviderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ("id", "name", "email")


class ServiceAreaDetailSerializer(serializers.ModelSerializer):
    provider = ProviderListSerializer

    class Meta:
        model = ServiceArea
        fields = "__all__"


class ProviderDetailSerializer(serializers.ModelSerializer):
    services_areas = ServiceAreaListSerializer(many=True)

    class Meta:
        model = Provider
        fields = "__all__"


class PolygonSerializer(serializers.Serializer):
    name = serializers.CharField()
    provider_name = serializers.CharField()
    price = serializers.DecimalField(max_digits=18, decimal_places=2)


class ServiceAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceArea
        fields = "__all__"


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = "__all__"
