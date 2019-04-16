from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings 

# Create your models here.
class Post(models.Model):
    content = models.CharField(max_length=100)
    # image = models.ImageField(blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #django m2m
    #위에서 user을 ForeignKey로 받기에 related_name을 사용, blank는 빈칸을 허용한다는 의미
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_post_set', blank=True)
    
class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    img = ProcessedImageField(
            upload_to='posts/images', #저장 위치
            processors=[ResizeToFill(600,600)], #크기 지정
            format='JPEG',
            options={'quality':100},
        )
    def __str__(self):
        return self.img

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    create_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-id',]