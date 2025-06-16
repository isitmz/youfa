from django.urls import path
from . import views

app_name = 'market'

#l'app market nelle Urls espone le API per i titoli
urlpatterns = [
    path('api/details/<str:ticker>/', views.get_asset_details, name='api_get_asset_details'), #path dell'API esposta
    path('api/price/<str:ticker>/', views.get_price_details, name='api_get_price'), #path dell'API esposta
    path('api/chart/<str:ticker>/', views.get_chart_data, name='get_chart_data'), #accetta due parametri/search query
    path("api/trade/", views.trade_asset, name="trade_asset"), #api per compravendita delle azioni da parte dell'User
    path('api/create-price-alert/', views.create_price_alert, name='create_price_alert'),#api per creare le notifiche da AJAX
    path('api/get-user-alerts/<str:ticker>/', views.get_user_alerts, name='get_user_alerts'),#api per prendere le notifiche di un utente in base al ticker
    path('api/delete-price-alert/', views.delete_price_alert, name='delete_price_alert'),#api per cancellare un alert utente in base al ticker
    path('', views.market_home, name='market_home'),
]
