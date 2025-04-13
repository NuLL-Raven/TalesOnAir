from django.urls import path
from . import views
from .views import authenticate_view

urlpatterns = [
    path('authenticate/', authenticate_view, name='authenticate'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('update-listening-time/', views.update_listening_time, name='update_listening_time'),
    path('get-completed-count/', views.get_completed_count, name='get_completed_count'),
]