from django.urls import path

from . import views

app_name='eggstra'
urlpatterns = [
    path('', views.overview, name='overview'),
    path('post/', views.post, name='post'),
    path('register/', views.register, name='register'),
    path('userprofile/', views.userprofile, name='userprofile'),
    path('<int:egg_available_id>/pickup/', views.pickup, name='pickup'),
    path('<int:egg_available_id>/remove/', views.remove, name='remove')
]