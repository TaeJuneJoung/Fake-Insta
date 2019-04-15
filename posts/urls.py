from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.list, name='list'),
    path('new/', views.new, name='new'),
    path('<int:id>/update/', views.update, name='update'),
    path('<int:id>/delete/', views.delete, name='delete'),
    path('<int:id>/comment/', views.comment_create, name='comment_create'),
    path('<int:id>/<int:c_id>/delete', views.comment_delete, name='comment_delete'),
    
    #like로 잡는 이유는 기능상 create와 delete기능을 두개를 동시 작업할 것이기에.
    path('<int:id>/like/', views.like, name='like'),
]