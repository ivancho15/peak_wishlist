from typing import Any

from django.db.models.query import QuerySet
from django.views.generic import  ListView
from peak_wishlist.models import Pais

class  PaisList(ListView):
    model = Pais 
    template_name = "peak_wishlist/paises.html"
    context_object_name = "paises"

    def get_queryset(self) -> QuerySet[Any]:
        continente = self.kwargs.get('continente')
        if continente:
            return Pais.objects.filter(continente=continente).order_by('nombre')
        return Pais.objects.order_by('nombre')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['continentes'] = Pais.Continente.choices
        context['continente_actual'] = self.kwargs.get('continente')
        return context