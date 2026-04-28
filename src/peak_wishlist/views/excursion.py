from typing import Any

from django.db.models import Q
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from peak_wishlist.models import Excursion, Montana, Proyecto, Ruta


class ExcursionList(ListView):
    model = Excursion
    template_name = "peak_wishlist/excursiones.html"
    context_object_name = "excursiones"

    def get_queryset(self) -> QuerySet[Any]:
        ruta_id = self.kwargs.get("ruta_id")
        proyecto_id = self.kwargs.get("proyecto_id")
        montana_id = self.kwargs.get("montana_id")

        if ruta_id:
            self.filtro = get_object_or_404(Ruta, id=ruta_id)
            queryset = Excursion.objects.filter(ruta=self.filtro).order_by(
                "-fecha_hora_inicio"
            )
        elif montana_id:
            self.filtro = get_object_or_404(Montana, id=montana_id)
            queryset = Excursion.objects.filter(ruta__montana=self.filtro).order_by(
                "-fecha_hora_inicio"
            )
        elif proyecto_id:
            self.filtro = get_object_or_404(Proyecto, id=proyecto_id)
            queryset = Excursion.objects.filter(proyecto=self.filtro).order_by(
                "-fecha_hora_inicio"
            )
        else:
            self.filtro = None
            queryset = Excursion.objects.all().order_by("-fecha_hora_inicio")

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(ruta__nombre__icontains=query) | Q(proyecto__nombre__icontains=query) 
                | Q(ruta__montana__nombre__icontains=query)
            )

        return queryset
        

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
