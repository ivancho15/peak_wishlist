from typing import Any

from django.views.generic import ListView, CreateView, DetailView
from django.shortcuts import get_object_or_404
from peak_wishlist.models import Parque, Pais
from django.urls import reverse_lazy
from peak_wishlist.forms import ParqueForm

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
        

class ParqueCreate(CreateView):
    model = Parque
    form_class = ParqueForm
    template_name = "peak_wishlist/parque_form.html"
    
    def form_valid(self, form):
        pais = get_object_or_404(Pais, id=self.kwargs.get('pais_id'))
        form.instance.pais = pais
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('peak_wishlist:parques_por_pais', kwargs={'pais_id': self.kwargs.get('pais_id')})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pais = get_object_or_404(Pais, id=self.kwargs.get('pais_id'))
        context['titulo_dinamico'] = f"🏞️ Registrar Parque/Area protegida en {pais.nombre}"
        context['url_cancelar'] = reverse_lazy('peak_wishlist:parques_por_pais', kwargs={'pais_id': self.kwargs.get('pais_id')})
        return context


    
