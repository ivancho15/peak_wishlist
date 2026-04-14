from django.urls import path
from peak_wishlist import views

app_name = 'peak_wishlist'

urlpatterns = [
    path('', views.index, name='index'),
]