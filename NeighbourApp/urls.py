from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('localnews/', views.local, name='local'),
    path('group/', views.group, name='group'),
]