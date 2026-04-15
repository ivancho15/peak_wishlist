from django.urls import path
from peak_wishlist import views

app_name = 'peak_wishlist'

urlpatterns = [
    path('', views.index, name='index'),
    path('paises/', views.paises, name='paises'),
    path('montanas/', views.montanas ,  name='montanas'),
    path('proyectos/', views.proyectos ,  name='proyectos'),
    path('excursiones', views.excursiones, name='excursiones'),
    path('pais/montanas/<int:pais_id>', views.montanas, name='montanas_por_pais'),
    path('proyecto/excursiones/<int:proyecto_id>', views.excursiones, name='excursiones_por_proyecto'),
    path('pais/parques/<int:pais_id>', views.parques, name='parques_por_pais')
    ]