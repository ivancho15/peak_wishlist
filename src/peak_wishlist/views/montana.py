from typing import Any

from django.db.models import Q
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from peak_wishlist.forms import MontanaForm
from peak_wishlist.models import Montana, Pais, Parque


class MontanaList(ListView):
    model = Montana
    template_name = "peak_wishlist/montanas.html"
    context_object_name = "montanas"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        pais_id = self.kwargs.get("pais_id")
        parque_id = self.kwargs.get("parque_id")

        if pais_id:
            self.filtro = get_object_or_404(Pais, id=pais_id)
            queryset = Montana.objects.filter(pais=self.filtro).order_by("-altitud")
        elif parque_id:
            self.filtro = get_object_or_404(Parque, id=parque_id)
            queryset = Montana.objects.filter(parque=self.filtro).order_by("-altitud")
        else:
            self.filtro = None
            queryset = Montana.objects.all().order_by("-altitud")

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query)
                | Q(cordillera__icontains=query)
                | Q(pais__nombre__icontains=query)
            )

        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        # comportamiento cuando se invoca el listado desde Pais    
        if isinstance(self.filtro, Pais):
            context["extension_titulo"] = f"en {self.filtro.nombre}"
            context["url_volver"] = reverse_lazy("peak_wishlist:paises")
            context["volver_label"] = "Volver a Países"
        # comportamiento cuando se invoca el listado desde Parque    
        elif isinstance(self.filtro, Parque):
            parque = self.filtro
            context["extension_titulo"] = f"en {parque.nombre} ({parque.pais})"
            context["url_volver"] = reverse_lazy(
                "peak_wishlist:parques_por_pais",
                kwargs={"pais_id": getattr(parque.pais, "pk", None)},
            )
            context["volver_label"] = "Volver a Parques"
        # comportamiento Listado General
        else:
            context["extension_titulo"] = ""
            context["url_volver"] = reverse_lazy("peak_wishlist:index")
            context["volver_label"] = "Volver al inicio"
        return context


class MontanaCreate(CreateView):
    model = Montana
    form_class = MontanaForm
    template_name = "peak_wishlist/montana_form.html"

    def get_success_url(self):
        if self.object and self.object.pais.exists():  # type: ignore
            primer_pais = self.object.pais.first()  # type: ignore
            return reverse_lazy(
                "peak_wishlist:montanas_por_pais", kwargs={"pais_id": primer_pais.id}
            )
        return reverse_lazy("peak_wishlist:montanas")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["url_cancelar"] = reverse_lazy("peak_wishlist:montanas")
        return context


class MontanaDetail(DetailView):
    model = Montana
    template_name = "peak_wishlist/montana_detail.html"
    context_object_name = "montana"
