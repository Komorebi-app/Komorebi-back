from unfold.admin import ModelAdmin

from .book import BookInline

class AuthorAdmin(ModelAdmin):
    list_display = ["pk", "lastname", "firstname"]
    search_fields = ["lastname", "firstname"]

    fieldsets = [
        (None, {"fields": ["lastname", "firstname", "biography"]}),
    ]

    inlines = [BookInline]
