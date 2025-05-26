from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


# class MyUser(AbstractUser):
#     pass


User = get_user_model()
