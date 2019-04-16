from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class User(AbstractUser):
    #'self'라고 써도 됨 -> settings.AUTH_USER_MODEL
    # related_name -> followers효과를 나타낸다.(역참조)
    # -> .user_set.all()로 접근할수도 있음
    followings = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="followers", blank=True)
    introduce = models.TextField()
    #카카오 계정과 연동을 위해 이름을 똑같이 씀
    profile_image = ProcessedImageField(
            upload_to='accounts/images', #저장 위치
            processors=[ResizeToFill(150,150)], #크기 지정
            format='JPEG',
            options={'quality':100},
            blank=True
        )
        
    def __str__(self):
        return self.username