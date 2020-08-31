from django.urls import path
from .views import ProfileDetailView  
from django.contrib.auth.views import LoginView
from core import views

app_name = 'core'

urlpatterns = [

    path('sellers/', views.sellers_signup, name='sellers-signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('login/', LoginView.as_view(), name='login'),
]