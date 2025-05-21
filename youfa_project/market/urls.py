from django.urls import path
from . import views

#l'app market nelle Urls espone le API per i titoli
urlpatterns = [
    path('api/details/<str:ticker>/', views.get_asset_details, name='api_get_asset_details'), #path dell'API esposta
    path('api/price/<str:ticker>/', views.get_price_details, name='api_get_price'), #path dell'API esposta
    path('api/chart/<str:ticker>/', views.get_chart_data, name='get_chart_data'), #accetta due parametri/search query
    path("api/trade/", views.trade_asset, name="trade_asset"), #api per compravendita delle azioni da parte dell'User
    path('', views.market_home, name='market_home'),
]
