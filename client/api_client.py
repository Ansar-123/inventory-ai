import requests

BASE_URL = "http://127.0.0.1:8000"


def get_products():

    response = requests.get(
        f"{BASE_URL}/products"
    )

    return response.json()