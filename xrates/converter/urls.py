from django.urls import path
from converter import views

urlpatterns = [
    path('', views.converter_view, name='converter'),
    path('history', views.convert_history_view, name='history'),
]
