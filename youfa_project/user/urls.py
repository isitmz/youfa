from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path("balance/recharge/", views.recharge_balance, name="recharge_balance"),
    path("api/notifications/",views.notifications_api, name='notifications_api'),
    path('password/change/', views.change_password, name='change_password'),
]
