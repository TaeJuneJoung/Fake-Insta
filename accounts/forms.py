from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

#User를 커스터마이징 한 후, join할때 UserCreationForm의 오류를 막기 위해 재설정
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        #패스워드를 입력하지 않아도 자동으로 쓰여진다.
        fields = ['username','email',]
        
class CustomUserChangeForm(UserChangeForm):
    #기본적으로 패스워드 수정도 보여주는데 그냥은 넘어갈수 없어서 잠시 None처리
    password = None
    class Meta:
        model = User
        fields = ['email', 'introduce', 'profile_image',]