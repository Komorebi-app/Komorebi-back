from unfold.admin import ModelAdmin

from .book import BookAuthorInline

class AuthorAdmin(ModelAdmin):
    list_display = ["pk", "lastname", "firstname"]
    search_fields = ["lastname", "firstname"]

    fieldsets = [
        (None, {"fields": ["lastname", "firstname", "biography"]}),
    ]

    inlines = [BookAuthorInline]
