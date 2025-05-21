from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  # Home app gestisce la pagina principale
    path('', include('core.urls')),  # Core app gestisce login e registrazione
    path('market/', include('market.urls')), # Market app gestisce le API yfinance
    path('user/', include('user.urls', namespace='user')), # app che gestisce le funzioni dell'user
    path('portfolio/', include('portfolio.urls')) # app che gestisce il portafoglio utente
]