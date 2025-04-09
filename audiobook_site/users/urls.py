from django.urls import path
from . import views
from .views import authenticate_view

urlpatterns = [
    path('authenticate/', authenticate_view, name='authenticate'),
    path('logout/', views.logout_view, name='logout'),
]
