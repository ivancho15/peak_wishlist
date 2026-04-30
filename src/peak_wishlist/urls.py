from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_not_required # type:ignore

from peak_wishlist.views import (
    excursion,
    montana,
    pais,
    parque,
    proyecto,
    refugio,
    ruta,
    user,
)

app_name = "peak_wishlist"

urlpatterns = [
    path(
        "",login_not_required(TemplateView.as_view(template_name="peak_wishlist/index.html")), name="index"
    ),
    path("paises/", pais.PaisList.as_view(), name="paises"),
    path('paises/continente/<str:continente>/', pais.PaisList.as_view(), name='paises_por_continente'),
    path(
        "pais/parques/<int:pais_id>/",
        parque.ParqueList.as_view(),
        name="parques_por_pais",
    ),
    path("pais/<int:pais_id>/parque/create/", parque.ParqueCreate.as_view(), name="registrar_parque"),
    path("parque/<int:pk>/", parque.ParqueDetail.as_view(), name="parque_detail"),
    path("montanas/", montana.MontanaList.as_view(), name="montanas"),
    path("montanas/create/", montana.MontanaCreate.as_view(), name="registrar_montana"),
    path("montana/<int:pk>/", montana.MontanaDetail.as_view(), name="montana_detail"),
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
    path("refugio/<int:pk>/", refugio.RefugioDetail.as_view(), name="refugio_detail"),
    path(
        "montana/rutas/<int:montana_id>/",
        ruta.RutaList.as_view(),
        name="rutas_por_montana",
    ),
    path(
        "montana/<int:montana_id>/ruta/create/", 
        ruta.RutaCreate.as_view(), 
        name="registrar_ruta"
    ),
    path("ruta/<int:pk>/", ruta.RutaDetail.as_view(), name="ruta_detail"),
    path(
        "ruta/obtener-dificultades/", 
        ruta.obtener_dificultades, 
        name="opciones_dificultades" 
    ),
    path("proyectos/", proyecto.ProyectoList.as_view(), name="proyectos"),
    path("proyecto/create/", proyecto.ProyectoCrate.as_view(), name="registrar_proyecto"),
    path("proyecto/<int:pk>/", proyecto.ProyectoDetail.as_view(), name="proyecto_detail"),
    path("proyecto/<int:pk>/update/", proyecto.ProyectoUpdate.as_view(), name="proyecto_update"),
    path("proyecto/<int:pk>/delete/", proyecto.ProyectoDelete.as_view(), name="proyecto_delete"),
    path("excursiones/", excursion.ExcursionList.as_view(), name="excursiones"),
    path("excursiones/create/", excursion.ExcursionCreate.as_view(), name="registrar_excursion"),
    path("excursion/<int:pk>/", excursion.ExcursionDetail.as_view(), name="excursion_detail"),
    path("excursion/<int:pk>/update/", excursion.ExcursionUpdate.as_view(), name="excursion_update"),
    path("excursion/<int:pk>/delete/", excursion.ExcursionDelete.as_view(), name="excursion_delete"),
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
        "montana/excursiones/<int:montana_id>/",
        excursion.ExcursionList.as_view(),
        name="excursiones_por_montana",
    ),
    path("login/", LoginView.as_view(template_name="peak_wishlist/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="peak_wishlist/logout.html"), name="logout"),
    path("register/", user.CustomRegisterView.as_view(), name="register"),
    path("profile/", user.Profile.as_view(), name="profile"),
]
