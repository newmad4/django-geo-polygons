from datetime import datetime, timedelta
from functools import lru_cache, wraps

from django.contrib.gis.geos import Point
from django.db.models import F
from rest_framework.utils.serializer_helpers import ReturnList

from provider.models import ServiceArea
from provider.serializers import PolygonSerializer

LATITUDE = "-?([1-8]?[1-9]|[1-9]0)\.{1}\d{1,6}"  # noqa: W605
LONGITUDE = "-?([1]?[1-7][1-9]|[1]?[1-8][0]|[1-9]?[0-9])\.{1}\d{1,6}"  # noqa: W605


class BaseCoordinateConvertor:
    regex = None

    def to_python(self, value) -> float:
        return float(value)

    def to_url(self, value) -> str:
        return str(value)


class LatConverter(BaseCoordinateConvertor):
    regex = LATITUDE


class LngConverter(BaseCoordinateConvertor):
    regex = LONGITUDE


def timed_lru_cache(seconds: int, maxsize: int = 128):
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache


@timed_lru_cache(2 * 60)
def get_services_areas_by_point(lat: float, lng: float) -> ReturnList:
    services_ares = (
        ServiceArea.objects.filter(geo_information__contains=Point(lat, lng))
        .annotate(provider_name=F("provider__name"))
        .only("name", "price")
        .all()
    )

    serializer = PolygonSerializer(instance=services_ares, many=True)
    return serializer.data
