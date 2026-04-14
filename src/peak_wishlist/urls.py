from django.urls import path
from peak_wishlist import views

app_name = 'peak_wishlist'

urlpatterns = [
    path('', views.index, name='index'),
    path('pais/', views.paises, name='pais'),
    path('montana/', views.montanas ,  name='montanas'),
    path('pais/montanas/<int:pais_id>', views.montanas, name='montanas_por_pais'),
    ]