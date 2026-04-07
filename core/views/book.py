from pydantic import ValidationError
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Book
from core.serializers import BookSerializer
from core.schemas import BookIsbnSchema
from core.services.google_books import (
    GoogleBooksNotConfiguredError,
    GoogleBooksRequestError,
    fetch_google_book_by_isbn,
)
from core.services.book import add_book_to_user_library, get_or_create_book
from core.utils.query import get_query_all_for_user


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Seuls les utilisateurs authentifiés peuvent accéder à cette vue
    permission_classes = [IsAuthenticated]

    # Override get_queryset pour filtrer les livres par utilisateur
    def get_queryset(self):
        return get_query_all_for_user(Book, self.request.user).order_by('id')


    # Action pour rechercher un livre par ISBN
    @action(detail=False, methods=['get'], url_path='search')
    def search_by_isbn(self, request):
        isbn = request.query_params.get('isbn')
        if not isbn:
            return Response({"error": "ISBN requis"}, status=status.HTTP_400_BAD_REQUEST)

        # Appel au service Google Books via ISBN
        try:
            data = fetch_google_book_by_isbn(isbn)
        except GoogleBooksNotConfiguredError:
            return Response(
                {"error": "Google Books non configuré: clé API manquante"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except GoogleBooksRequestError:
            return Response(
                {"error": "Erreur Google Books: service indisponible"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        if data:
            return Response(data)
        return Response({"error": "Livre non trouvé"}, status=status.HTTP_404_NOT_FOUND)


    @action(detail=False, methods=['post'], url_path='add-to-library')
    def add_to_library(self, request):
        """
        Ajoute un livre trouvé par ISBN à la bibliothèque de l'utilisateur.
        """
        try:
            # On valide les données brutes avec Pydantic
            validated_schema = BookIsbnSchema(**request.data)

            # On récupère l'ISBN formatté par le serializer
            isbn = validated_schema.isbn

        except ValidationError as e:
            # On renvoie les erreurs Pydantic au format DRF (400 Bad Request)
            return Response(e.errors(), status=status.HTTP_400_BAD_REQUEST)

        try:
            data = fetch_google_book_by_isbn(isbn)
        except GoogleBooksNotConfiguredError:
            return Response(
                {"error": "Google Books non configuré: clé API manquante"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except GoogleBooksRequestError:
            return Response(
                {"error": "Erreur Google Books: service indisponible"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        if not data:
            return Response({"error": "Livre non trouvé"}, status=status.HTTP_404_NOT_FOUND)

        # Créer ou récupérer le livre en base via la méthode du service  book.py
        book, _ = get_or_create_book(data, isbn)

        # Ajouter le livre à la bibliothèque de l'utilisateur
        add_book_to_user_library(request.user, book)

        book = self.get_serializer(book)
        return Response(book.data, status=status.HTTP_201_CREATED)
