from django.contrib import admin
from django.contrib.auth.models import User

from core.admin.author import AuthorAdmin
from core.admin.book import BookAdmin
from core.admin.library import LibraryAdmin
from core.admin.user import UserAdmin

from core.models.author import Author
from core.models.book import Book
from core.models.library import Library

admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Library, LibraryAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
