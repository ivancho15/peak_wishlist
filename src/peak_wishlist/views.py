from django.shortcuts import render
from peak_wishlist import models

def index(request):
    return render(request, 'peak_wishlist/index.html')

def paises(request):
    query = models.Pais.objects.all()
    return render(request, "peak_wishlist/pais.html", {'paises': query})

def montanas(request, pais_id=None):
    if pais_id:
        pais =  models.Pais.objects.get(id =pais_id)
        query = models.Montana.objects.filter(pais=pais)
        extension_titulo = f" en {pais.nombre}"
    else:
        query = models.Montana.objects.all()
        extension_titulo = " "
    return render(request, "peak_wishlist/montana.html", {'montanas': query, "extension_titulo": extension_titulo})