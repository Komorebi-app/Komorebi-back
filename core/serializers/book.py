from rest_framework import serializers

from core.models import Book

class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'language', 'pages', 'published', 'resume']

class AddBookToLibrarySerializer(serializers.Serializer):
    # Definition d'un champ ISBN pour que DRF puisse trouver le champ dans le body de la requête
    isbn = serializers.CharField(
        max_length=13,
    )

    def validate_isbn(self, value):
        # Formattage de l'ISBN pour avoir le format de la BDD (sans tirets ni espaces)
        isbn = value.replace('-', '').replace(' ', '')  

        # Vérification du format de l'ISBN (10 ou 13 chiffres)
        if not (len(isbn) == 10 or len(isbn) == 13) or not isbn.isdigit():
            raise serializers.ValidationError("Le format de l'ISBN doit être de 10 ou 13 chiffres.")    

        return isbn
