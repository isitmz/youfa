# portfolio/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/portfolio-info/<str:ticker>/', views.portfolio_info, name='portfolio_info'),
]