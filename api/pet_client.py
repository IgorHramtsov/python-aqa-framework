import requests

from config.config import BASE_API_URL, REQUEST_TIMEOUT


class PetClient:

    def __init__(self):
        self.session = requests.Session()

    def close(self):
        self.session.close()

    def create_pet(self, payload: dict):
        return self.session.post(
            f"{BASE_API_URL}/pet",
            json=payload,
            timeout=REQUEST_TIMEOUT
        )

    def get_pet(self, pet_id: int):
        return self.session.get(
            f"{BASE_API_URL}/pet/{pet_id}",
            timeout=REQUEST_TIMEOUT
        )

    def update_pet(self, payload: dict):
        return self.session.put(
            f"{BASE_API_URL}/pet",
            json=payload,
            timeout=REQUEST_TIMEOUT
        )

    def get_pets_by_status(self, status: str):
        return self.session.get(
            f"{BASE_API_URL}/pet/findByStatus",
            params={"status": status},
            timeout=REQUEST_TIMEOUT
        )

    def delete_pet(self, pet_id: int):
        return self.session.delete(
            f"{BASE_API_URL}/pet/{pet_id}",
            timeout=REQUEST_TIMEOUT
        )
