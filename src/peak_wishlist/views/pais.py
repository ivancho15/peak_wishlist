from typing import Any

from django.db.models import Q
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import ListView

from peak_wishlist.models import Pais
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_not_required # type:ignore

@method_decorator(login_not_required, name='dispatch')
class PaisList(ListView):
    model = Pais
    template_name = "peak_wishlist/paises.html"
    context_object_name = "paises"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        continente = self.kwargs.get("continente")
        if continente:
            queryset = Pais.objects.filter(continente=continente)
        else:
            queryset = Pais.objects.all()

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(Q(nombre__icontains=query))
        return queryset.order_by("nombre")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["continentes"] = Pais.Continente.choices
        context["continente_actual"] = self.kwargs.get("continente")
        context["url_volver"] = reverse_lazy("peak_wishlist:index")
        context["volver_label"] = "Volver al inicio"
        return context
