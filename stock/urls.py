from django.urls import path
from stock import views

urlpatterns = [
    path('add_stockdata', views.add_data),
    path('get_stockdata',views.get_data),
    path('delete_stockdata',views.delete_data),
]

