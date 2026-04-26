from typing import Any

from django.db.models.query import QuerySet
from django.views.generic import CreateView,  DeleteView, DetailView, ListView, UpdateView
from django.shortcuts import get_object_or_404
from peak_wishlist.models import Parque, Pais

class  ParqueList(ListView):
    model = Parque
    template_name = "peak_wishlist/parques.html"
    context_object_name = "parques"

    def get_queryset(self):
        self.pais = get_object_or_404(Pais, id=self.kwargs['pais_id'])
        return Parque.objects.filter(pais=self.pais).order_by('nombre')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['extension_titulo'] = f"en {self.pais.nombre}"
        return context
        