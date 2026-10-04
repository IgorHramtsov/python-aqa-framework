import pytest
import allure

from data.pet_factory import (
    create_pet_payload,
    create_invalid_pet_payload
)

pytestmark = pytest.mark.api


def assert_pet_matches(actual: dict, expected: dict):
    assert actual["id"] == expected["id"], (
        f"Expected id {expected['id']}, got {actual['id']}"
    )
    assert actual["name"] == expected["name"], (
        f"Expected name '{expected['name']}', got '{actual['name']}'"
    )
    assert actual["status"] == expected["status"], (
        f"Expected status '{expected['status']}', got '{actual['status']}'"
    )
    assert actual["category"] == expected["category"], (
        f"Expected category {expected['category']}, got {actual['category']}"
    )
    assert actual["photoUrls"] == expected["photoUrls"], (
        f"Expected photoUrls {expected['photoUrls']}, got {actual['photoUrls']}"
    )
    assert actual["tags"] == expected["tags"], (
        f"Expected tags {expected['tags']}, got {actual['tags']}"
    )


@allure.feature("Pet API")
@allure.story("Create pet")
@allure.title("Create pet with valid data")
@pytest.mark.smoke
def test_create_pet(pet_client, pet_cleanup):
    payload = create_pet_payload()
    pet_cleanup.append(payload["id"])

    response = pet_client.create_pet(payload)

    assert response.status_code == 200, (
        f"Failed to create pet {payload['id']}. "
        f"Expected 200, got {response.status_code}. "
        f"Response: {response.text}"
    )

    body = response.json()

    assert_pet_matches(body, payload)


def test_get_pet_by_id(pet_client, created_pet):
    pet_id = created_pet["id"]
    response = pet_client.get_pet(pet_id)

    assert response.status_code == 200, (
        f"Failed to get pet {pet_id}. "
        f"Expected 200, got {response.status_code}. "
        f"Response: {response.text}"
    )

    body = response.json()

    assert_pet_matches(body, created_pet)


def test_update_pet(pet_client, created_pet):
    updated_pet = created_pet.copy()
    updated_pet["name"] = "qwerty"
    updated_pet["status"] = "pending"

    update_response = pet_client.update_pet(updated_pet)
    assert update_response.status_code == 200, (
        f"Failed to update pet {updated_pet['id']} "
        f"Expected 200, got {update_response.status_code}. "
        f"Response: {update_response.text}"
    )

    assert_pet_matches(update_response.json(), updated_pet)

    get_response = pet_client.get_pet(updated_pet["id"])
    assert get_response.status_code == 200, (
        f"Failed to get updated pet {updated_pet['id']}.  "
        f"Expected 200, got {get_response.status_code}. "
        f"Response: {get_response.text}"
    )

    assert_pet_matches(get_response.json(), updated_pet)


@pytest.mark.parametrize("status", [
    "available",
    "pending",
    "sold"
])
def test_get_pets_by_status(pet_client, pet_cleanup, status):
    payload = create_pet_payload(status=status)
    pet_cleanup.append(payload["id"])

    create_response = pet_client.create_pet(payload)

    assert create_response.status_code == 200, (
        f"Failed to prepare pet with status '{status}'. "
        f"Expected 200, got {create_response.status_code}. "
        f"Response: {create_response.text}"
    )

    response = pet_client.get_pets_by_status(status)

    assert response.status_code == 200, (
        f"Failed to get pets by status '{status}'. "
        f"Expected 200, got {response.status_code}. "
        f"Response: {response.text}"
    )

    pets = response.json()

    assert isinstance(pets, list), (
        f"Expected response body to be list, "
        f"got {type(pets).__name__}"
    )

    assert any(pet["id"] == payload["id"] for pet in pets), (
        f"Created pet {payload['id']} was not found "
        f"in response for status '{status}'"
    )

    for pet in pets:
        assert pet["status"] == status, (
            f"Pet {pet.get('id')} has unexpected status. "
            f"Expected '{status}', got '{pet.get('status')}'"
        )


def test_get_nonexistent_pet(pet_client):
    nonexistent_pet_id = 1002023020

    response = pet_client.get_pet(nonexistent_pet_id)
    assert response.status_code == 404, (
        f"Expected pet {nonexistent_pet_id} to be nonexistent. "
        f"Expected 404, got {response.status_code}. "
        f"Response: {response.text}"
    )


def test_delete_pet_and_get_deleted_pet(pet_client, created_pet):
    pet_id = created_pet["id"]

    delete_response = pet_client.delete_pet(pet_id)
    assert delete_response.status_code == 200, (
        f"Failed to delete pet {pet_id}. "
        f"Expected 200, got {delete_response.status_code}. "
        f"Response: {delete_response.text}"
    )

    get_response = pet_client.get_pet(pet_id)
    assert get_response.status_code == 404, (
        f"Deleted pet {pet_id} is still accessible. "
        f"Expected 404, got {get_response.status_code}. "
        f"Response: {get_response.text}"
    )


def test_create_pet_with_invalid_id_type(pet_client):
    payload = create_invalid_pet_payload()

    response = pet_client.create_pet(payload)
    assert response.status_code == 400, (
        f"Expected validation error for invalid pet id. "
        f"Expected 400, got {response.status_code}. "
        f"Response: {response.text}"
    )
