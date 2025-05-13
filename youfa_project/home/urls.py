from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # La home page dell'app
]