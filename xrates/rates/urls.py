from django.urls import path

from rates import views

urlpatterns = [
    path('', views.rates_view),
    path('rates/', views.rates_view, name='rates'),
]
