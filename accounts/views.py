from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from posts.forms import CommentForm

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("posts:list")
    else:
        # title = "Sign Up"
        form = CustomUserCreationForm()
    return render(request, "accounts/form.html", {"form":form})
    
def login(request):
    if request.method == "POST":
        #AuthenticationForm은 알아서 User을 찾기에 커스터마이징해도 그대로 사용가능
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("posts:list")
    else:
        # title = "Login"
        form = AuthenticationForm()
    return render(request, "accounts/form.html", {"form":form})
    
def logout(request):
    auth_logout(request)
    return redirect("posts:list")
    
def user_page(request, id):
    #get_user_model을 사용하는 이유
    # : .models로 가져오면 모델명이 바뀌더라도 변경할 필요가 없어서
    User = get_user_model()
    user_info = User.objects.get(username=id)
    user = request.user
    comment_form = CommentForm()
    return render(request, "accounts/user_page.html", {"user_info":user_info, "user":user, "comment_form":comment_form})

@login_required
def follow(request, id):
    me = request.user
    User = get_user_model()
    star = User.objects.get(username=id)
    
    if me != star:
        if star in me.followings.all():
            #취소
            me.followings.remove(star)
        else:
            #추가
            me.followings.add(star)
            
    return redirect("accounts:user_page", id)
    