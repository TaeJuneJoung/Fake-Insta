from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    #'self'라고 써도 됨 -> settings.AUTH_USER_MODEL
    # related_name -> followers효과를 나타낸다.(역참조)
    # -> .user_set.all()로 접근할수도 있음
    followings = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="followers", blank=True)
        
    def __str__(self):
        return self.username