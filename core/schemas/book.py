from pydantic import BaseModel, validator


class BookIsbnSchema(BaseModel):
    isbn: str

    @validator("isbn")
    @classmethod
    # Ajout de cls afin de représenter la classe elle même dans le décorateur @validator
    def validate_isbn(cls, value):
        # Formattage de l'ISBN pour avoir le format de la BDD (sans tirets ni espaces)
        isbn = value.replace('-', '').replace(' ', '')
        # Vérification du format de l'ISBN (10 ou 13 chiffres)
        if not (len(isbn) in (10, 13)) or not isbn.isdigit():
            raise ValueError("Le format de l'ISBN doit être de 10 ou 13 chiffres.")
        return isbn


class BookManualSchema(BaseModel):
    isbn: str
    title: str
    author: str
    language: str = ''
    pages: int = 0
    published: str | None = None # Peut être optionnel et si pas renseigné, on laisse à None
    resume: str | None = None
    cover_url: str | None = None

    @validator("isbn")
    @classmethod
    def validate_isbn(cls, value):
        isbn = value.replace('-', '').replace(' ', '')
        if not (len(isbn) in (10, 13)) or not isbn.isdigit():
            raise ValueError("Le format de l'ISBN doit être de 10 ou 13 chiffres.")
        return isbn

    @validator("title", "author")
    @classmethod
    def validate_required_text(cls, value):
        formatted = value.strip() # Supprimer les espaces en début et fin de chaîne
        if not formatted:
            raise ValueError("Ce champ est obligatoire.")
        return formatted
