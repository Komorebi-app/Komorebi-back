import requests
from django.conf import settings


GOOGLE_BOOKS_BASE_URL = "https://www.googleapis.com/books/v1/volumes"
GOOGLE_BOOKS_REQUEST_TIMEOUT = 10


def fetch_google_book_by_isbn(isbn: str):
    api_key = getattr(settings, "GOOGLE_BOOKS_API_KEY", "")
    if not api_key:
        return None

    try:
        response = requests.get(
            GOOGLE_BOOKS_BASE_URL,
            params={"q": f"isbn:{isbn}", "key": api_key},
            timeout=GOOGLE_BOOKS_REQUEST_TIMEOUT,
        )
        response.raise_for_status()
    except requests.RequestException:
        return None

    data = response.json()
    if data and "items" in data:
        return data["items"][0]["volumeInfo"]

    return None