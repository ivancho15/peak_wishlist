from typing import Any

from django.db.models import Q
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from peak_wishlist.models import Excursion, Montana, Proyecto, Ruta
from peak_wishlist.forms import ExursionForm
from django.urls import reverse_lazy

##listado de Excursiones
class ExcursionList(ListView):
    model = Excursion
    template_name = "peak_wishlist/excursiones.html"
    context_object_name = "excursiones"

    def get_queryset(self) -> QuerySet[Any]:
        """
        maneja el listado de excursiones segun el filtro aplicado: por Ruta, montaña o  proyecto 
        """
        ruta_id = self.kwargs.get("ruta_id")
        proyecto_id = self.kwargs.get("proyecto_id")
        montana_id = self.kwargs.get("montana_id")

        if ruta_id:
            self.filtro = get_object_or_404(Ruta, id=ruta_id)
            queryset = Excursion.objects.filter(ruta=self.filtro).order_by(
                "-fecha_hora_inicio"
            )
        elif montana_id:
            self.filtro = get_object_or_404(Montana, id=montana_id)
            queryset = Excursion.objects.filter(ruta__montana=self.filtro).order_by(
                "-fecha_hora_inicio"
            )
        elif proyecto_id:
            self.filtro = get_object_or_404(Proyecto, id=proyecto_id)
            queryset = Excursion.objects.filter(proyecto=self.filtro).order_by(
                "-fecha_hora_inicio"
            )
        else:
            self.filtro = None
            queryset = Excursion.objects.all().order_by("-fecha_hora_inicio")

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(ruta__nombre__icontains=query) | Q(proyecto__nombre__icontains=query) 
                | Q(ruta__montana__nombre__icontains=query)
            )

        return queryset
        

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        Pobla el contexto segun el filtro aplicado en la busqueda de Excursiones
        """
        context = super().get_context_data(**kwargs)

        if isinstance(self.filtro, Ruta):
            context["extension_titulo"] = (
                f"para la ruta {self.filtro.nombre} en {self.filtro.montana.nombre}"
            )
        elif isinstance(self.filtro, Montana):
            context["extension_titulo"] = (
                f"en {self.filtro.nombre}"
            )
        elif isinstance(self.filtro, Proyecto):
            context["extension_titulo"] = f"en el proyecto {self.filtro.nombre}"
        else:
            context["extension_titulo"] = ""

        return context


#Detalle de Excrusion 
class ExcursionDetail(DetailView):
    model = Excursion
    template_name = "peak_wishlist/excursion_detail.html"
    context_object_name = "excursion"


#Borrar Excursion 
class ExcursionDelete(DeleteView):
    model = Excursion
    template_name = "peak_wishlist/excursion_confirm_delete.html"
    success_url = "/excursiones/"


#Actualizacion de Excrusion 
class ExcursionUpdate(UpdateView):
    model = Excursion
    template_name = "peak_wishlist/excursion_form.html"
    form_class = ExursionForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs() #type: ignore
        if self.object: #type: ignore
            kwargs.update({
                'p_id': self.object.proyecto.id if self.object.proyecto else None,  #type: ignore
                'r_id': self.object.ruta.id if self.object.ruta else None, #type: ignore
                'm_id': self.object.ruta.montana.id if (self.object.ruta and self.object.ruta.montana) else None,#type: ignore
            })
        return kwargs

    def get_success_url(self):
        r_id = self.request.GET.get('r_id')
        m_id = self.request.GET.get('m_id')
        p_id = self.request.GET.get('p_id')

        if p_id: return reverse_lazy("peak_wishlist:proyecto_detail", kwargs={"pk": p_id})
        if r_id: return reverse_lazy("peak_wishlist:ruta_detail", kwargs={"pk": r_id})
        if m_id: return reverse_lazy("peak_wishlist:montana_detail", kwargs={"pk": m_id})
        
        if self.object: #type: ignore 
            return reverse_lazy("peak_wishlist:excursion_detail", kwargs={"pk": self.object.pk}) #type: ignore

        return reverse_lazy("peak_wishlist:excursiones")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # El botón cancelar ahora es más estable
        referer = self.request.META.get('HTTP_REFERER')
        context["url_cancelar"] = referer if referer else reverse_lazy("peak_wishlist:excursiones")
        return context


#Registrar excursion 
class ExcursionCreate(CreateView):
    model = Excursion
    form_class = ExursionForm
    template_name = "peak_wishlist/excursion_form.html"

    def get_form_kwargs(self):
        # pasa la ID de la URL al formulario
        kwargs = super().get_form_kwargs()
        kwargs['m_id'] = self.request.GET.get('m_id')
        kwargs['p_id'] = self.request.GET.get('p_id')
        kwargs['r_id'] = self.request.GET.get('r_id')
        return kwargs

    def get_success_url(self):
        m_id = self.request.GET.get('m_id')
        p_id = self.request.GET.get('p_id')
        r_id = self.request.GET.get('r_id')

        if p_id:
            return reverse_lazy("peak_wishlist:proyecto_detail", kwargs={"pk": p_id})

        if r_id:
            return reverse_lazy("peak_wishlist:ruta_detail", kwargs={"pk": r_id})

        if m_id:
            return reverse_lazy("peak_wishlist:montana_detail", kwargs={"pk": m_id})

        return reverse_lazy("peak_wishlist:excursiones")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # El botón cancelar ahora es más estable
        referer = self.request.META.get('HTTP_REFERER')
        context["url_cancelar"] = referer if referer else reverse_lazy("peak_wishlist:excursiones")
        return context
