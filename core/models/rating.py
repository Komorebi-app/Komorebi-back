from django.core.validators import MaxLengthValidator, MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db import models
from django.forms import Textarea

from .book import Book

class Rating(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    comment = models.TextField(
        help_text="Write a comment in a maximum of 1000 characters.",
        max_length=1000,
        validators=[MaxLengthValidator(1000)],
    )

    RATING_CHOICES = [
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★'),
    ]
    note = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )

    formfield_overrides = {
        models.TextField: {
            "widget": Textarea(attrs={
                "rows": 5, 
                "class": "border-red-500",
                "maxlength": "1000",
            })
        },
    }

    def __str__(self):
        return self.user.get_full_name() if self.user != None else 'Anonymous'
