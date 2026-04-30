from typing import Any

from django.db.models import Q
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from peak_wishlist.forms import RutaForm
from peak_wishlist.models import Montana, Ruta
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_not_required # type:ignore

@method_decorator(login_not_required, name='dispatch')
class RutaList(ListView):
    model = Ruta
    template_name = "peak_wishlist/rutas.html"
    context_object_name = "rutas"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        montana_id = self.kwargs.get("montana_id")
        if montana_id:
            self.montana = get_object_or_404(Montana, id=montana_id)
            queryset = Ruta.objects.filter(montana=self.montana).order_by("nombre")
        else:
            self.montana = None
            queryset = Ruta.objects.all().order_by("nombre")

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(Q(nombre__icontains=query))

        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.montana:
            context["extension_titulo"] = f"en {self.montana.nombre}"
            context["url_volver"] = reverse_lazy(
                "peak_wishlist:montana_detail",
                kwargs={"pk": self.montana.pk},
            )
            context["volver_label"] = f"Volver a {self.montana.nombre}"
        else:
            context["extension_titulo"] = ""
            context["url_volver"] = reverse_lazy("peak_wishlist:index")
            context["volver_label"] = "Volver al inicio"
        return context

class RutaCreate(CreateView):
    model = Ruta
    form_class = RutaForm
    template_name = "peak_wishlist/ruta_form.html"

    def form_valid(self, form):
        montana = get_object_or_404(Montana, id=self.kwargs.get("montana_id"))
        form.instance.montana = montana
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "peak_wishlist:rutas_por_montana",
            kwargs={"montana_id": self.kwargs.get("montana_id")},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        montana = get_object_or_404(Montana, id=self.kwargs.get("montana_id"))
        context["titulo_dinamico"] = f"🥾 Registrar Ruta en {montana.nombre}"
        context["url_cancelar"] = reverse_lazy(
            "peak_wishlist:rutas_por_montana",
            kwargs={"montana_id": self.kwargs.get("montana_id")},
        )
        return context

@method_decorator(login_not_required, name='dispatch')
class RutaDetail(DetailView):
    model = Ruta
    template_name = "peak_wishlist/ruta_detail.html"
    context_object_name = "ruta"


# Obtener dificultades segun actividad
def obtener_dificultades(request):
    actividad = request.GET.get("actividad")
    mapeo = {
        Ruta.TipoActividad.ALTA_MONTANA: Ruta.DificultadAltaMontana.choices,
        Ruta.TipoActividad.TREKKING: Ruta.DificultadSenderismo.choices,
        Ruta.TipoActividad.ESCALADA_EN_ROCA: Ruta.DificultadEscalada.choices,
        Ruta.TipoActividad.MTB: Ruta.DificultadMTB.choices,
    }
    opciones = mapeo.get(actividad, [])

    return render(request,"peak_wishlist/componentes/dificultad_opciones.html",{"opciones": opciones},
    )
