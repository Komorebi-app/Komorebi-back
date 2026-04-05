import requests
from django.conf import settings


GOOGLE_BOOKS_BASE_URL = "https://www.googleapis.com/books/v1/volumes"
GOOGLE_BOOKS_REQUEST_TIMEOUT = 10


class GoogleBooksNotConfiguredError(Exception):
    pass


class GoogleBooksRequestError(Exception):
    pass


def fetch_google_book_by_isbn(isbn: str):
    # Vérifie la configuration locale
    api_key = getattr(settings, "GOOGLE_BOOKS_API_KEY", "")
    if not api_key:
        raise GoogleBooksNotConfiguredError("GOOGLE_BOOKS_API_KEY manquant")

    # Appelle Google Books
    try:
        response = requests.get(
            GOOGLE_BOOKS_BASE_URL,
            params={"q": f"isbn:{isbn}", "key": api_key},
            timeout=GOOGLE_BOOKS_REQUEST_TIMEOUT,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise GoogleBooksRequestError("Erreur lors de l'appel Google Books") from exc

    # Analyse la réponse
    try:
        data = response.json()
    except ValueError as exc:
        raise GoogleBooksRequestError("Réponse JSON invalide de Google Books") from exc

    try:
        # Si Google ne trouve pas de livre
        if not data.get("items"):
            return None

        # Si la réponse n'a pas les infos attendues
        first_item = data["items"][0]
        volume_info = first_item.get("volumeInfo")
        if not volume_info:
            raise GoogleBooksRequestError("Le champ 'volumeInfo' est manquant")
    except (AttributeError, KeyError, IndexError, TypeError) as exc:
        raise GoogleBooksRequestError("Format de réponse Google Books invalide") from exc

    # Livre trouvé
    return volume_info