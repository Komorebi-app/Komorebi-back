from unfold.admin import ModelAdmin, TabularInline

from core.models import Book

class BookAdmin(ModelAdmin):
    list_display = ["isbn", "title", "author", "language", "pages", "published"]
    list_filter = ["language"]
    search_fields = ["isbn", "title", "author"]

class BookInline(TabularInline):
    model = Book
    verbose_name = 'Book'
    verbose_name_plural = 'Books'
    extra = 0
