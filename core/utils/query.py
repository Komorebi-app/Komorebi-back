from django.db import models

from core.utils.types import AnyUser

def get_query_all_for_user(model: models.Model, user: AnyUser):
    return model.objects.all() if user.is_superuser else model.objects.all().filter(client=user)
