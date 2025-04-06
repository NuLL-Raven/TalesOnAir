from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.sign_up, name='sign_up'),
    path('sign-in/', views.sign_in, name='sign_in'),
    path('logout/', LogoutView.as_view(next_page='sign_in'), name='logout'),
]
