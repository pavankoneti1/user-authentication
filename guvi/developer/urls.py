from django.urls import path
from .views import *
urlpatterns =[
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login', login, name='login'),
    path('profile', profile, name='profile'),
    path('edit/', edit, name='edit'),
    path('task/', TaskList, name='task'),
]