import pytest
import allure

from data.pet_factory import (
    create_pet_payload,
    create_invalid_pet_payload
)

pytestmark = pytest.mark.api


@allure.feature("Pet API")
@allure.story("Create pet")
@allure.title("Create pet with valid data")
@pytest.mark.smoke
def test_create_pet(pet_client):
    payload = create_pet_payload()
    response = pet_client.create_pet(payload)
    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}. "
        f"Response: {response.text}"
    )

    body = response.json()
    assert body["id"] == payload["id"]
    assert body["name"] == payload["name"]
    assert body["status"] == payload["status"]
    assert body["category"]["id"] == payload["category"]["id"]
    assert body["category"]["name"] == payload["category"]["name"]
    assert body["photoUrls"] == payload["photoUrls"]
    assert body["tags"] == payload["tags"]


def test_get_pet_by_id(pet_client, created_pet):
    pet_id = created_pet["id"]
    response = pet_client.get_pet(pet_id)

    assert response.status_code == 200
    assert response.json()["id"] == pet_id


def test_update_pet(pet_client, created_pet):
    updated_pet = created_pet.copy()
    updated_pet["name"] = "qwerty"
    updated_pet["status"] = "pending"

    response = pet_client.update_pet(updated_pet)
    assert response.status_code == 200

    body = response.json()
    assert body["id"] == updated_pet["id"]
    assert body["name"] == updated_pet["name"]
    assert body["status"] == updated_pet["status"]


@pytest.mark.parametrize("status", [
    "available",
    "pending",
    "sold"])
def test_get_pets_by_status(pet_client, status):
    response = pet_client.get_pets_by_status(status)
    assert response.status_code == 200

    pets = response.json()

    for pet in pets:
        assert pet["status"] == status


def test_get_non_existent_pet(pet_client):
    nonexistent_pet_id = 1002023020
    response = pet_client.get_pet(nonexistent_pet_id)
    assert response.status_code == 404


def test_delete_pet_and_get_deleted_pet(pet_client, created_pet):
    pet_id = created_pet["id"]
    response = pet_client.delete_pet(pet_id)
    assert response.status_code == 200
    response = pet_client.get_pet(pet_id)
    assert response.status_code == 404


def test_create_pet_with_invalid_id_type(pet_client):
    payload = create_invalid_pet_payload()
    response = pet_client.create_pet(payload)
    assert response.status_code == 400
