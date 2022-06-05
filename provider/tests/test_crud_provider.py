import pytest
from django.urls import reverse
from faker import Faker

from provider.models import Provider

fake = Faker()


@pytest.mark.django_db
class TestCRUDProviderAPI:
    @pytest.fixture
    def detail_first_provider_url(self, first_provider) -> str:
        return reverse("provider:providers-detail", args=(first_provider.id,))

    @pytest.fixture
    def general_provider_url(self) -> str:
        return reverse("provider:providers-list")

    @pytest.fixture
    def payload_for_create(self) -> dict:
        return {
            "name": fake.name(),
            "email": fake.email(),
            "phone_number": fake.phone_number(),
            "language": "en-us",
            "currency": "USD",
        }

    @pytest.fixture
    def payload_for_full_update(self) -> dict:
        return {
            "name": fake.name(),
            "email": fake.email(),
            "phone_number": fake.phone_number(),
            "language": "en-us",
            "currency": "USD",
        }

    @pytest.fixture
    def payload_for_partial_update(self) -> dict:
        return {
            "name": fake.name(),
            "email": fake.email(),
        }

    def test_get_provider(self, client, first_provider, detail_first_provider_url) -> None:
        response = client.get(detail_first_provider_url)

        assert response.status_code == 200

        response_json = response.json()
        assert response_json == {
            "id": first_provider.id,
            "name": first_provider.name,
            "email": first_provider.email,
            "phone_number": first_provider.phone_number,
            "language": first_provider.language,
            "currency": first_provider.currency,
            "services_areas": list(first_provider.services_areas.all()),
        }

    def test_get_list_providers(self, client, first_provider, second_provider, general_provider_url) -> None:
        response = client.get(general_provider_url)

        assert response.status_code == 200

        response_json = response.json()
        assert response_json.get("count") == len([first_provider, second_provider])

    def test_create_provider(self, client, general_provider_url, payload_for_create) -> None:
        old_count_of_providers = Provider.objects.count()
        response = client.post(general_provider_url, data=payload_for_create)

        assert response.status_code == 201

        new_count_of_providers = Provider.objects.count()
        assert new_count_of_providers == old_count_of_providers + 1

    def test_partial_update_provider(
        self, client, detail_first_provider_url, payload_for_partial_update, first_provider
    ) -> None:
        response = client.patch(
            detail_first_provider_url,
            data=payload_for_partial_update,
            content_type="application/json"
        )

        assert response.status_code == 200

        updated_provider = Provider.objects.get(id=first_provider.id)
        for field_name, value in payload_for_partial_update.items():
            assert getattr(updated_provider, field_name) == value

    def test_full_update_provider(
        self, client, detail_first_provider_url, payload_for_full_update, first_provider
    ) -> None:
        response = client.put(
            detail_first_provider_url,
            data=payload_for_full_update,
            content_type="application/json"
        )

        assert response.status_code == 200

        updated_provider = Provider.objects.get(id=first_provider.id)
        for field_name, value in payload_for_full_update.items():
            assert getattr(updated_provider, field_name) == value

    def test_delete_provider(self, client, detail_first_provider_url) -> None:
        old_count_of_providers = Provider.objects.count()
        response = client.delete(detail_first_provider_url)

        assert response.status_code == 204

        new_count_of_providers = Provider.objects.count()
        assert new_count_of_providers == old_count_of_providers - 1
