import pytest
from django.contrib.gis.geos import Polygon
from model_bakery import baker

from provider.models import Provider, ServiceArea


@pytest.fixture
def first_provider(db):
    return baker.make(Provider)


@pytest.fixture
def second_provider(db):
    return baker.make(Provider)


@pytest.fixture
def first_providers_area(db, first_provider):
    geo_information = Polygon(
        (
            (0.0, 0.0),
            (0.0, 50.0),
            (50.0, 50.0),
            (50.0, 0.0),
            (0.0, 0.0)
        )
    )
    return baker.make(ServiceArea, provider=first_provider, geo_information=geo_information)


@pytest.fixture
def second_providers_area(db, second_provider):
    geo_information = Polygon(
        (
            (0.0, 0.0),
            (0.0, 80.0),
            (80.0, 80.0),
            (80.0, 0.0),
            (0.0, 0.0)
        )
    )
    return baker.make(ServiceArea, provider=second_provider, geo_information=geo_information)


@pytest.fixture
def point_in_polygons():
    return 10.12345, 11.12345


@pytest.fixture
def point_not_in_polygons():
    return -10.12345, -11.12345

