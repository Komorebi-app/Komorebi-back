from django.contrib.auth.models import User

from core.models import Book, Author, Library


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

    author, _ = Author.objects.get_or_create(
        first_name=first_name,
        last_name=last_name
    )

    return author

def get_or_create_book(data: dict, isbn: str):
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

    # Récupérer l'URL de la couverture du livre
    image_links = volume_info.get('imageLinks', {})
    cover_url = image_links.get('thumbnail') or image_links.get('smallThumbnail')

    # Récupérer ou créer le livre dans la base de données
    book, created = Book.objects.get_or_create(
        isbn=isbn,
        defaults={
            'title': volume_info.get('title', 'Sans titre'),
            'language': volume_info.get('language', ''),
            'pages': volume_info.get('pageCount', 0),
            'published': volume_info.get('publishedDate', None),
            'resume': volume_info.get('description', ''),
            'cover_url': cover_url,
            'author': author,
        }
    )

    return book, created


def get_or_create_manual_book(data: dict):
    """
    Crée ou récupère un livre à partir des données du formulaire manuel.
    """
    author = get_or_create_author(data['author'])

    book, created = Book.objects.get_or_create(
        isbn=data['isbn'],
        defaults={
            'title': data['title'],
            'language': data.get('language', ''),
            'pages': data.get('pages', 0),
            'published': data.get('published'),
            'resume': data.get('resume'),
            'cover_url': data.get('cover_url'),
            'author': author,
        }
    )

    return book, created

def add_book_to_user_library(user: User, book: Book):
    """
    Associe un livre à la bibliothèque d'un utilisateur.
    Crée la bibliothèque si elle n'existe pas encore.
    """
    # Récupérer ou créer la collection de l'utilisateur
    library, _ = Library.objects.get_or_create(user=user)

    # Lier le livre à la bibliothèque (relation Many-To-Many)
    book.library.add(library)

    return library
