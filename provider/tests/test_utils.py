import pytest
from faker import Faker

from provider.utils import get_services_areas_by_point

fake = Faker()


@pytest.mark.django_db
class TestUtils:
    def test_get_services_areas_by_included_point(
        self, first_providers_area, second_providers_area, point_in_polygons
    ) -> None:
        lat, lng = point_in_polygons
        expects_fields_in_response_objects = {"name", "provider_name", "price"}

        polygons = get_services_areas_by_point(lat, lng)
        assert len(polygons) == len([first_providers_area, second_providers_area])
        assert set(polygons[0].keys()) == expects_fields_in_response_objects

    def test_get_services_areas_by_not_included_point(
        self, first_providers_area, point_not_in_polygons
    ) -> None:
        lat, lng = point_not_in_polygons

        polygons = get_services_areas_by_point(lat, lng)
        assert polygons == []
