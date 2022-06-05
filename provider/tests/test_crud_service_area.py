import pytest
from django.contrib.gis.geos import Polygon
from django.urls import reverse
from faker import Faker

from provider.models import ServiceArea

fake = Faker()


@pytest.mark.django_db
class TestCRUDServiceAreaAPI:
    @pytest.fixture
    def detail_service_area_url(self, first_providers_area) -> str:
        return reverse("provider:services-ares-detail", args=(first_providers_area.id,))

    @pytest.fixture
    def general_service_area_url(self) -> str:
        return reverse("provider:services-ares-list")

    @pytest.fixture
    def geo_information(self) -> Polygon:
        return Polygon(
            (
                (0.0, 0.0),
                (0.0, 75.0),
                (75.0, 75.0),
                (75.0, 0.0),
                (0.0, 0.0)
            )
        )

    @pytest.fixture
    def payload_for_create(self, first_provider, geo_information) -> dict:
        return {
            "name": fake.name(),
            "provider": first_provider.id,
            "price": fake.pydecimal(left_digits=3, right_digits=2, positive=True),
            "geo_information": geo_information.__str__(),
        }

    @pytest.fixture
    def payload_for_full_update(self, first_provider, geo_information) -> dict:
        return {
            "name": fake.name(),
            "provider": first_provider.id,
            "price": fake.pydecimal(left_digits=3, right_digits=2, positive=True),
            "geo_information": geo_information.__str__(),
        }

    @pytest.fixture
    def payload_for_partial_update(self) -> dict:
        return {
            "price": fake.pydecimal(left_digits=3, right_digits=2, positive=True),
        }

    def test_get_service_area(self, client, first_providers_area, detail_service_area_url) -> None:
        response = client.get(detail_service_area_url)

        assert response.status_code == 200

        response_json = response.json()
        assert response_json == {
            "id": first_providers_area.id,
            "name": first_providers_area.name,
            "provider": first_providers_area.provider_id,
            "price": first_providers_area.price.__str__(),
            "geo_information": first_providers_area.geo_information,
        }

    def test_get_list_services_areas(
        self, client, first_providers_area, second_providers_area, general_service_area_url
    ) -> None:
        response = client.get(general_service_area_url)

        assert response.status_code == 200

        response_json = response.json()
        assert response_json.get("count") == len([first_providers_area, second_providers_area])

    def test_create_service_area(self, client, general_service_area_url, payload_for_create) -> None:
        old_count_of_services_areas = ServiceArea.objects.count()
        response = client.post(general_service_area_url, data=payload_for_create)

        assert response.status_code == 201

        new_count_of_services_areas = ServiceArea.objects.count()
        assert new_count_of_services_areas == old_count_of_services_areas + 1

    def test_partial_update_service_area(
        self, client, detail_service_area_url, payload_for_partial_update, first_providers_area
    ) -> None:
        response = client.patch(
            detail_service_area_url,
            data=payload_for_partial_update,
            content_type="application/json"
        )

        assert response.status_code == 200

        updated_service_area = ServiceArea.objects.get(id=first_providers_area.id)
        for field_name, value in payload_for_partial_update.items():
            assert getattr(updated_service_area, field_name) == value

    def test_full_update_service_area(
        self, client, detail_service_area_url, payload_for_full_update, first_providers_area, geo_information
    ) -> None:
        response = client.put(
            detail_service_area_url,
            data=payload_for_full_update,
            content_type="application/json"
        )

        assert response.status_code == 200

        updated_service_area = ServiceArea.objects.get(id=first_providers_area.id)
        assert updated_service_area.provider_id == payload_for_full_update["provider"]
        assert updated_service_area.name == payload_for_full_update["name"]
        assert updated_service_area.price == payload_for_full_update["price"]
        assert updated_service_area.geo_information.coords == geo_information.coords

    def test_delete_service_area(self, client, detail_service_area_url) -> None:
        old_count_of_service_area = ServiceArea.objects.count()
        response = client.delete(detail_service_area_url)

        assert response.status_code == 204

        new_count_of_service_area = ServiceArea.objects.count()
        assert new_count_of_service_area == old_count_of_service_area - 1
