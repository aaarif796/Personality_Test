from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_view
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('profile/',views.profile,name='profile'),
    path('login/',auth_view.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout',auth_view.LogoutView.as_view(template_name='logout.html'),name='logout'),
    path('sentiment1/',views.sentimentWord,name='sentimentWord'),
    path('p_test/',views.p_test,name='p_test'),
    path('languagetrans/',views.languagetrans,name='languagetrans')
]

