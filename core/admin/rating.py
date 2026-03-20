from unfold.admin import TabularInline

from core.models import Rating

class RatingInline(TabularInline):
    model = Rating
    verbose_name = 'Rating'
    verbose_name_plural = 'Ratings'
    extra = 0
