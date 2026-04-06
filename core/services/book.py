from core.models import Book, Author, Library
from core.services.google_books import fetch_google_book_by_isbn
from django.contrib.auth.models import User


def get_or_create_author(authors: str):
    """
    Récupère l'auteur d'un livre. 
    Crée l'auteur si il n'existe pas encore.
    """
    # Séparer le nom en first_name et last_name
    names = authors.strip().split()
    
    if len(names) >= 2:
        first_name = names[0]
        last_name = ' '.join(names[1:])  # Au cas où il y a plusieurs prénoms/noms
    else:
        first_name = names[0]
        last_name = ''
    
    author, created = Author.objects.get_or_create(
        first_name=first_name,
        last_name=last_name
    )

    return author

def get_or_create_book(data: dict):
    """
    Récupère un livre de l'API google. 
    Crée le livre si celui-ci n'est pas trouvé.
    """
    volume_info = data.get('volumeInfo', data)

    # On récupère la liste des auteurs, ou une liste par défaut si vide
    authors_list = volume_info.get('authors', ['Auteur Inconnu'])
    author_name = authors_list[0]

    # Récupérer ou créer l'auteur via le service
    author = get_or_create_author(author_name)

    # Extraire l'identifiant unique (ISBN) depuis la liste des industryIdentifiers pour pouvoir faire get_or_create
    identifiers = volume_info.get('industryIdentifiers', [])
    isbn = identifiers[0]['identifier'] if identifiers else None

    # Récupérer ou créer le livre dans la base de données
    book, created = Book.objects.get_or_create(
        isbn=isbn,
        defaults={
            'title': volume_info.get('title', 'Sans titre'),
            'language': volume_info.get('language', ''),
            'pages': volume_info.get('pageCount', 0),
            'published': volume_info.get('publishedDate', None),
            'resume': volume_info.get('description', ''),
            'author': author,
        }
    )

    return book, created

def add_book_to_user_library(user: User, book: Book):
    """
    Associe un livre à la bibliothèque d'un utilisateur. 
    Crée la bibliothèque si elle n'existe pas encore.
    """

    # Récupérer ou crér la collection de l'utilisateur

    library, created = Library.objects.get_or_create(user=user)

    # Lier le livre à la bibliothèque (relation Many-To-Many)
    book.library.add(library)

    return library
    
