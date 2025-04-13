from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('search/', views.search_page, name='search_page'),
    path('search/live/', views.live_search, name='live_search'),
]
