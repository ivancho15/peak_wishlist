from typing import Any

from django.db.models import Q
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from peak_wishlist.forms import ParqueForm
from peak_wishlist.models import Pais, Parque


class ParqueList(ListView):
    model = Parque
    template_name = "peak_wishlist/parques.html"
    context_object_name = "parques"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        self.pais = get_object_or_404(Pais, id=self.kwargs["pais_id"])
        queryset = Parque.objects.filter(pais=self.pais).order_by("nombre")

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(Q(nombre__icontains=query))

        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["extension_titulo"] = f"en {self.pais.nombre}"
        context["url_volver"] = reverse_lazy("peak_wishlist:paises")
        context["volver_label"] = "Volver a Países"
        return context


class ParqueCreate(CreateView):
    model = Parque
    form_class = ParqueForm
    template_name = "peak_wishlist/parque_form.html"

    def form_valid(self, form):
        pais = get_object_or_404(Pais, id=self.kwargs.get("pais_id"))
        form.instance.pais = pais
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "peak_wishlist:parques_por_pais",
            kwargs={"pais_id": self.kwargs.get("pais_id")},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pais = get_object_or_404(Pais, id=self.kwargs.get("pais_id"))
        context["titulo_dinamico"] = (
            f"🏞️ Registrar Parque/Area protegida en {pais.nombre}"
        )
        context["url_cancelar"] = reverse_lazy(
            "peak_wishlist:parques_por_pais",
            kwargs={"pais_id": self.kwargs.get("pais_id")},
        )
        return context


class ParqueDetail(DetailView):
    model = Parque
    template_name = "peak_wishlist/parque_detail.html"
    context_object_name = "parque"
