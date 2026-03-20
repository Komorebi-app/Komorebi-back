from typing import Union

from django.contrib.auth.models import User, AnonymousUser

AnyUser = Union[User, AnonymousUser]
