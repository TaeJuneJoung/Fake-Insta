from django import forms
from .models import Post, Image, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = '__all__'
        fields = ['content',]

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        # fields = '__all__' #사용자에게 보여줄 필요가 없는 부분까지 나옴
        fields = ['img',]
        widgets = {
            'img' : forms.FileInput(attrs={'multiple':True,'id':"upload"}) #TextInput() / FileInput()
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]