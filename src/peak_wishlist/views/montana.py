from typing import Any

from django.db.models.query import QuerySet
from django.views.generic import  ListView, DetailView, CreateView
from peak_wishlist.models import Montana, Pais, Parque
from django.shortcuts import get_object_or_404
from peak_wishlist.forms import MontanaForm
from django.urls import reverse_lazy

class  MontanaList(ListView):
    model = Montana
    template_name = "peak_wishlist/montanas.html"
    context_object_name = "montanas"

    def get_queryset(self) -> QuerySet[Any]:
        pais_id = self.kwargs.get('pais_id')
        parque_id = self.kwargs.get('parque_id')
    
        if pais_id:
            self.filtro = get_object_or_404(Pais, id=pais_id)
            return Montana.objects.filter(pais=self.filtro).order_by('-altitud')
        elif parque_id:
            self.filtro  = get_object_or_404(Parque, id=parque_id)
            return Montana.objects.filter(parque=self.filtro).order_by('-altitud')
        
        self.filtro = None
        return Montana.objects.all().order_by('-altitud')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context  = super().get_context_data(**kwargs)
        
        if isinstance(self.filtro, Pais):
            context['extension_titulo'] = f"en {self.filtro.nombre}"
        elif isinstance (self.filtro, Parque):
            context['extension_titulo'] = f"en {self.filtro.nombre} ({self.filtro.pais})"
        else:
            context['extension_titulo'] = ""
        return context


class MontanaCreate(CreateView):
    model = Montana
    form_class = MontanaForm
    template_name = "peak_wishlist/montana_form.html" 

    def get_success_url(self):
        if self.object and self.object.pais.exists(): # type: ignore
            primer_pais = self.object.pais.first() # type: ignore
            return reverse_lazy('peak_wishlist:montanas_por_pais', kwargs={'pais_id': primer_pais.id})
        return reverse_lazy('peak_wishlist:montanas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_cancelar'] = reverse_lazy('peak_wishlist:montanas')
        return context