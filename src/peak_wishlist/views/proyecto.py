from django.views.generic import CreateView,  DeleteView, DetailView, ListView, UpdateView
from peak_wishlist.models import Proyecto

class ProyectoList(ListView):
    model = Proyecto
    template_name = "peak_wishlist/proyectos.html"
    