import pytest
from django.urls import reverse
from faker import Faker

fake = Faker()


@pytest.mark.django_db
class TestPolygonAPI:
    @pytest.fixture
    def point_in_polygons_url(self, point_in_polygons) -> str:
        lat, lng = point_in_polygons
        return reverse("provider:polygons", args=(lat, lng))

    @pytest.fixture
    def point_not_in_polygons_url(self, point_not_in_polygons) -> str:
        lat, lng = point_not_in_polygons
        return reverse("provider:polygons", args=(lat, lng))

    def test_get_all_polygons_by_included_point(
        self, client, point_in_polygons_url, first_providers_area, second_providers_area
    ) -> None:
        expects_fields_in_response_objects = {"name", "provider_name", "price"}
        response = client.get(point_in_polygons_url)

        assert response.status_code == 200

        response_json = response.json()
        assert type(response_json).__name__ == "list"
        assert len(response_json) == len([first_providers_area, second_providers_area])
        assert set(response_json[0].keys()) == expects_fields_in_response_objects

    def test_get_all_polygons_by_not_included_point(
        self, client, point_not_in_polygons_url, first_providers_area, second_providers_area
    ) -> None:
        response = client.get(point_not_in_polygons_url)

        assert response.status_code == 200

        response_json = response.json()
        assert type(response_json).__name__ == "list"
        assert len(response_json) == 0
