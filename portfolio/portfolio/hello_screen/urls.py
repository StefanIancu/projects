from hello_screen import views
from django.urls import path

urlpatterns = [
    path('', views.hello_screen, name='hello_world'),
]