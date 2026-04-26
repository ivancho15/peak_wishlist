from typing import Any

from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from peak_wishlist.models import Excursion, Proyecto, Ruta


class ExcursionList(ListView):
    model = Excursion
    template_name = "peak_wishlist/excursiones.html"
    context_object_name = "excursiones"

    def get_queryset(self) -> QuerySet[Any]:
        ruta_id = self.kwargs.get("ruta_id")
        proyecto_id = self.kwargs.get("proyecto_id")

        if ruta_id:
            self.filtro = get_object_or_404(Ruta, id=ruta_id)
            return Excursion.objects.filter(ruta=self.filtro).order_by(
                "-fecha_hora_inicio"
            )
        elif proyecto_id:
            self.filtro = get_object_or_404(Proyecto, id=proyecto_id)
            return Excursion.objects.filter(proyecto=self.filtro).order_by(
                "-fecha_hora_inicio"
            )

        self.filtro = None
        return Excursion.objects.all().order_by("-fecha_hora_inicio")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        if isinstance(self.filtro, Ruta):
            context["extension_titulo"] = (
                f"para la ruta {self.filtro.nombre} en {self.filtro.montana.nombre}"
            )
        elif isinstance(self.filtro, Proyecto):
            context["extension_titulo"] = f"en el proyecto {self.filtro.nombre}"
        else:
            context["extension_titulo"] = ""

        return context
