from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    
    path('user_page/<str:id>/', views.user_page, name="user_page"),
    path('edit_profile/<str:id>/', views.edit_profile, name="edit_profile"),
    
    path('follow/<str:id>/', views.follow, name="follow"),
]