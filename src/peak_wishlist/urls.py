from django.urls import path
from django.views.generic import TemplateView

from peak_wishlist.views import (
    excursion,
    montana,
    pais,
    parque,
    proyecto,
    refugio,
    ruta,
)

app_name = "peak_wishlist"

urlpatterns = [
    path(
        "", TemplateView.as_view(template_name="peak_wishlist/index.html"), name="index"
    ),
    path("paises/", pais.PaisList.as_view(), name="paises"),
    path('paises/continente/<str:continente>/', pais.PaisList.as_view(), name='paises_por_continente'),
    path(
        "pais/parques/<int:pais_id>/",
        parque.ParqueList.as_view(),
        name="parques_por_pais",
    ),
    path("pais/<int:pais_id>/parques/create/", parque.ParqueCreate.as_view(), name="registrar_parque"),
    path("montanas/", montana.MontanaList.as_view(), name="montanas"),
    path("montanas/create/", montana.MontanaCreate.as_view(), name="registrar_montana"),
    path("proyectos/", proyecto.ProyectoList.as_view(), name="proyectos"),
    path("excursiones/", excursion.ExcursionList.as_view(), name="excursiones"),
    path(
        "pais/montanas/<int:pais_id>/",
        montana.MontanaList.as_view(),
        name="montanas_por_pais",
    ),
    path(
        "proyecto/excursiones/<int:proyecto_id>/",
        excursion.ExcursionList.as_view(),
        name="excursiones_por_proyecto",
    ),
    path(
        "montana/rutas/<int:montana_id>/",
        ruta.RutaList.as_view(),
        name="rutas_por_montana",
    ),
    path(
        "parque/montanas/<int:parque_id>/",
        montana.MontanaList.as_view(),
        name="montanas_por_parque",
    ),
    path(
        "ruta/excursiones/<int:ruta_id>/",
        excursion.ExcursionList.as_view(),
        name="excursiones_por_ruta",
    ),
    path(
        "montana/refugios/<int:montana_id>/",
        refugio.RefugioList.as_view(),
        name="refugios_por_montana",
    ),
    path(
        "montana/<int:montana_id>/refugios/create/", 
        refugio.RefugioCreate.as_view(), 
        name="registrar_refugio"
    ),
    path(
        "montana/excursiones/<int:montana_id>/",
        excursion.ExcursionList.as_view(),
        name="excursiones_por_montana",
    ),
]
