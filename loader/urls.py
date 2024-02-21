from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('validate/', views.validate, name='validate'),
    path('wallet/', views.wallet, name="wallet")
]
