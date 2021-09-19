from django.urls import path

from . import views

app_name='eggstra'
urlpatterns = [
    path('', views.overview, name='overview'),
    path('eggpost/', views.eggpost, name='eggpost'),
    path('register/', views.register, name='register'),
    path('user_delete/', views.user_delete, name='user_delete'),
    path('profile/', views.profile, name='profile'),
    path('<int:eggpost_id>/pickup/', views.pickup, name='pickup'),
    path('<int:eggpost_id>/update/', views.eggpost_update, name='update'),
    path('<int:eggpost_id>/delete/', views.eggpost_delete, name='delete')
]