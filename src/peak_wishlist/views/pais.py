from typing import Any

from django.db.models.query import QuerySet
from django.views.generic import  ListView
from peak_wishlist.models import Pais
from django.db.models import Q


class  PaisList(ListView):
    model = Pais 
    template_name = "peak_wishlist/paises.html"
    context_object_name = "paises"

    def get_queryset(self) -> QuerySet[Any]:
        continente = self.kwargs.get('continente')
        if continente:
            queryset = Pais.objects.filter(continente=continente)
        else:
            queryset = Pais.objects.all()

        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(nombre__icontains=query))
        return queryset.order_by('nombre')
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['continentes'] = Pais.Continente.choices
        context['continente_actual'] = self.kwargs.get('continente')
        return context