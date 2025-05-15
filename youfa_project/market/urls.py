from django.urls import path
from . import views

urlpatterns = [
    path('api/details/<str:ticker>/', views.get_asset_details, name='api_get_asset_details'), #path dell'API esposta
    path('api/price/<str:ticker>/', views.get_price_details, name='api_get_price'), #path dell'API esposta
    path('api/chart/<str:ticker>/', views.get_chart_data, name='get_chart_data'), #accetta due parametri/search query
    path('', views.market_home, name='market_home'),
]
