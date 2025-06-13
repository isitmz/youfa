# portfolio/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/portfolio-info/<str:ticker>/', views.portfolio_info, name='portfolio_info'),
    path('api/portfolio-balance/', views.get_saldo, name='get_saldo'),
]