from rest_framework import viewsets
from core.models import Book
from core.serializers import BookSerializer
from core.utils.query import get_query_all_for_user
from rest_framework import permissions, response, status
from rest_framework.decorators import action
from core.services.google_books import fetch_google_book_by_isbn


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Seuls les utilisateurs authentifiés peuvent accéder à cette vue
    permission_classes = [permissions.IsAuthenticated]

    # Override get_queryset pour filtrer les livres par utilisateur
    def get_queryset(self):
        return get_query_all_for_user(Book, self.request.user).order_by('id')


    # Action pour rechercher un livre par ISBN
    @action(detail=False, methods=['get'], url_path='search')
    def search_by_isbn(self, request):
        isbn = request.query_params.get('isbn')
        if not isbn:
            return response.Response({"error": "ISBN requis"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Appel au service Google Books via ISBN
        data = fetch_google_book_by_isbn(isbn)
        
        if data:
            return response.Response(data)
        return response.Response({"error": "Livre non trouvé"}, status=status.HTTP_404_NOT_FOUND)