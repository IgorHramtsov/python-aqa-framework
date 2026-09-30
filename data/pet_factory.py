import time


def create_pet_payload(
        name: str = "MyPet",
        status: str = "available"
) -> dict:
    return {
        "id": time.time_ns(),
        "name": name,
        "category": {
            "id": 1,
            "name": "Dogs"
        },
        "photoUrls": ["string"],
        "tags": [
            {
                "id": 0,
                "name": "string"
            }
        ],
        "status": status
    }


def create_invalid_pet_payload() -> dict:
    payload = create_pet_payload()
    payload["id"] = "hello"
    return payload
