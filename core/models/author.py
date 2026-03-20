from django.core.validators import MaxLengthValidator
from django.db import models
from django.forms import Textarea

class Author(models.Model):
    biography = models.TextField(
        blank=True,
        null=True,
        help_text="Write a short presentation in a maximum of 1500 characters.",
        max_length=1500,
        validators=[MaxLengthValidator(1500)],
    )
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)

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
        return f"{self.firstname} {self.lastname}"
