import pytest
from requests import RequestException

from api.pet_client import PetClient
from data.pet_factory import create_pet_payload


@pytest.fixture
def pet_client():
    client = PetClient()
    try:
        yield client
    finally:
        client.close()


@pytest.fixture
def pet_cleanup(pet_client):
    pet_ids = []
    yield pet_ids

    errors = []
    for pet_id in pet_ids:
        try:
            response = pet_client.delete_pet(pet_id)
        except RequestException as error:
            errors.append(f"Cleanup failed for pet {pet_id}: {error}")
            continue

        if response.status_code not in (200, 404):
            errors.append(
                f"Cleanup failed for pet {pet_id}. "
                f"Expected 200 or 404, got {response.status_code}. "
                f"Response: {response.text}"
            )

    assert not errors, "\n".join(errors)


@pytest.fixture
def created_pet(pet_client, pet_cleanup):
    payload = create_pet_payload()
    pet_cleanup.append(payload["id"])
    response = pet_client.create_pet(payload)

    assert response.status_code == 200, (
        f"Failed to create pet {payload['id']} in setup. "
        f"Expected 200, got {response.status_code}. "
        f"Response: {response.text}"
    )

    return payload
