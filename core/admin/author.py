from unfold.admin import ModelAdmin

from .book import BookAuthorInline

class AuthorAdmin(ModelAdmin):
    list_display = ["pk", "last_name", "first_name"]
    search_fields = ["last_name", "first_name"]

    fieldsets = [
        (None, {"fields": ["last_name", "first_name", "biography"]}),
    ]

    inlines = [BookAuthorInline]
