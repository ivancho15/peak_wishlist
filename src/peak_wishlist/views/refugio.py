from typing import Any

from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from peak_wishlist.models import Montana, Refugio


class RefugioList(ListView):
    model = Refugio
    template_name = "peak_wishlist/refugios.html"
    context_object_name = "refugios"

    def get_queryset(self) -> QuerySet[Any]:
        montana_id = self.kwargs.get("montana_id")
        if montana_id:
            self.montana = get_object_or_404(Montana, id=montana_id)
            return Refugio.objects.filter(montana=self.montana).order_by("nombre")
        self.montana = None
        return Refugio.objects.all().order_by("nombre")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.montana:
            context["extension_titulo"] = f"en {self.montana.nombre}"
        else:
            context["extension_titulo"] = ""
        return context
