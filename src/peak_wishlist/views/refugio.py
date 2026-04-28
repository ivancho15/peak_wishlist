from typing import Any

from django.db.models import Q
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from peak_wishlist.forms import RefugioForm
from peak_wishlist.models import Montana, Refugio


class RefugioList(ListView):
    model = Refugio
    template_name = "peak_wishlist/refugios.html"
    context_object_name = "refugios"

    def get_queryset(self) -> QuerySet[Any]:
        montana_id = self.kwargs.get("montana_id")
        if montana_id:
            self.montana = get_object_or_404(Montana, id=montana_id)
            queryset = Refugio.objects.filter(montana=self.montana).order_by("nombre")
        else:
            self.montana = None
            queryset = Refugio.objects.all().order_by("nombre")

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(Q(nombre__icontains=query))

        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.montana:
            context["extension_titulo"] = f"en {self.montana.nombre}"
        else:
            context["extension_titulo"] = ""
        return context


class RefugioCreate(CreateView):
    model = Refugio
    form_class = RefugioForm
    template_name = "peak_wishlist/refugio_form.html"

    def get_initial(self):
        initial = super().get_initial()
        montana = get_object_or_404(Montana, id=self.kwargs.get("montana_id"))
        initial["montana"] = montana
        return initial

    def form_valid(self, form):
        form.instance.montana = get_object_or_404(
            Montana, id=self.kwargs.get("montana_id")
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "peak_wishlist:refugios_por_montana",
            kwargs={"montana_id": self.kwargs.get("montana_id")},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        montana = get_object_or_404(Montana, id=self.kwargs.get("montana_id"))
        context["titulo_dinamico"] = f"🛖 Registrar Refugio en {montana.nombre}"
        context["url_cancelar"] = reverse_lazy("peak_wishlist:montanas")
        return context
