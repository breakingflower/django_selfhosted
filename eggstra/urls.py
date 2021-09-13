from django.urls import path

from . import views

app_name='eggstra'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('<int:egg_available_id>/details/', views.details, name='details'),
    path('<int:egg_available_id>/pickup/', views.pickup, name='pickup'),
    path('<int:egg_available_id>/remove/', views.remove, name='remove')
]