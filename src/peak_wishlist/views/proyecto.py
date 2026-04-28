from typing import Any

from django.db.models import Q
from django.db.models.query import QuerySet
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from peak_wishlist.models import Proyecto


class ProyectoList(ListView):
    model = Proyecto
    template_name = "peak_wishlist/proyectos.html"
    context_object_name = "proyectos"

    def get_queryset(self) -> QuerySet[Any]:
        queryset = Proyecto.objects.all().order_by("-fecha_inicio")

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(Q(nombre__icontains=query) | Q(pais_destino__nombre__icontains=query))

        return queryset


class ProyectoDetail(DetailView):
    model = Proyecto
    template_name = "peak_wishlist/proyecto_detail.html"
    context_object_name = "proyecto"


class ProyectoUpdate(UpdateView):
    model = Proyecto
    template_name = "peak_wishlist/proyecto_form.html"
    fields = "__all__"
    success_url = "/proyectos/"


class ProyectoDelete(DeleteView):
    model = Proyecto
    template_name = "peak_wishlist/proyecto_confirm_delete.html"
    success_url = "/proyectos/"
