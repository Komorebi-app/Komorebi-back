from django.contrib import admin

from unfold.admin import ModelAdmin

class LibraryAdmin(ModelAdmin):
    list_display = ["pk", "user", "get_book_count"]
    search_fields = ["user"]

    @admin.display(
        description="Book count",
    )
    def get_book_count(self, obj):
        return obj.book_set.count()
