from django.contrib import admin
from .models import Post, Image, Hashtag

# Register your models here.
admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Hashtag)