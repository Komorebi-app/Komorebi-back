from unfold.admin import ModelAdmin, TabularInline

from core.admin.rating import RatingInline
from core.models import Book

class BookAdmin(ModelAdmin):
    list_display = ["isbn", "title", "author", "language", "pages", "published", "resume"]
    list_filter = ["language"]
    search_fields = ["isbn", "title", "author"]

    inlines = [RatingInline]

class BookAuthorInline(TabularInline):
    model = Book
    fields = ["title", "isbn", "language", "published"]
    extra = 0

class BookLibraryInline(TabularInline):
    model = Book.library.through
    extra = 0
    verbose_name = "Book"
    verbose_name_plural = "Books"
