from pydantic import BaseModel, validator


class BookIsbnSchema(BaseModel):
    isbn: str

    @validator("isbn")
    def validate_isbn(value):
        # Formattage de l'ISBN pour avoir le format de la BDD (sans tirets ni espaces)
        isbn = value.replace('-', '').replace(' ', '')
        # Vérification du format de l'ISBN (10 ou 13 chiffres)
        if not (len(isbn) in (10, 13)) or not isbn.isdigit():
            raise ValueError("Le format de l'ISBN doit être de 10 ou 13 chiffres.")
        return isbn
