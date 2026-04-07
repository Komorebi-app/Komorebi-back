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



def fetch_google_book_by_title(title: str):
    # Vérifie la configuration locale
    api_key = getattr(settings, "GOOGLE_BOOKS_API_KEY", "")
    if not api_key:
        raise GoogleBooksNotConfiguredError("GOOGLE_BOOKS_API_KEY manquant")

    # Appelle Google Books
    try:
        response = requests.get(
            GOOGLE_BOOKS_BASE_URL,
            params={"q": f"intitle:{title}", "key": api_key},
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
            return []

        # On extrait le volumeInfo de chaque livre trouvé
        books = []
        for item in data["items"]:
            volume_info = item.get("volumeInfo")
            identifiers = volume_info.get('industryIdentifiers', [])

            # On cherche l'ISBN_13 d'abord, sinon l'ISBN_10
            isbn_val = next((id['identifier'] for id in identifiers if id['type'] in ['ISBN_13', 'ISBN_10']), None)

            # On n'ajoute le livre à la liste que s'il a un ISBN pour pouvoir dans le futur l'ajouter à la BDD via le front
            if isbn_val:
                volume_info['isbn'] = isbn_val # On ajoute l'ISBN au volume_info pour faciliter son utilisation côté front ( pour un futur ajout de la part de l'utilisateur)
                books.append(volume_info)

            # si pas d'isbn, books.append n'est pas appelé et le livre n'est pas ajouté à la liste des résultats

        if not books:
            raise GoogleBooksRequestError("Le champ 'volumeInfo' est manquant")
    except (AttributeError, KeyError, IndexError, TypeError) as exc:
        raise GoogleBooksRequestError("Format de réponse Google Books invalide") from exc

    # Livres trouvés
    return books

