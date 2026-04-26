from django.views.generic import CreateView,  DeleteView, DetailView, ListView, UpdateView
from peak_wishlist.models import Pais

class  PaisList(ListView):
    model = Pais 
    template_name = "peak_wishlist/paises.html"


    