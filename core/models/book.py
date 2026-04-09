from django.contrib import admin

from django.core.validators import MaxLengthValidator, RegexValidator
from django.template.defaultfilters import truncatechars
from django.db import models
from django.forms import Textarea
from django.core.validators import MaxValueValidator, MinValueValidator

from .author import Author
from .library import Library

class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    library = models.ManyToManyField(Library)

    isbn = models.CharField(
        verbose_name="ISBN",
        max_length=13,
        unique=True,
        help_text="Format: 10 or 13 digits",
        validators=[RegexValidator(
            regex=r'^(?:\d{10}|\d{13})$',
            message="The ISBN must contain exactly 10 or 13 digits.",
            code='invalid_isbn'
        )]
    )
    language = models.CharField(max_length=2)
    pages = models.PositiveIntegerField()
    published = models.DateField(verbose_name="Date published", null=True, blank=True)
    resume = models.TextField(
        blank=True,
        null=True,
        help_text="Describe the work in a maximum of 1500 characters.",
        max_length=1500,
        validators=[MaxLengthValidator(1500)],
    )
    cover_url = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=100)

    progress = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        default=0
    )

    formfield_overrides = {
        models.TextField: {
            "widget": Textarea(attrs={
                "rows": 5, 
                "class": "border-red-500",
                "maxlength": "1500",
            })
        },
    }

    def __str__(self):
        return str(self.title)

    @admin.display(description= "resume")
    def getResume(self):
        return truncatechars(self.resume, 100)

    @admin.display(description= "image")
    def getCoverUrl(self):
        return truncatechars(self.cover_url, 50)

Book.library.through.__str__ = lambda x: f"{x.book.isbn}"
