from django.shortcuts import render
from peak_wishlist import models

def index(request):
    return render(request, 'peak_wishlist/index.html')

def paises(request):
    query = models.Pais.objects.all().order_by('nombre')
    return render(request, "peak_wishlist/paises.html", {'paises': query})

def montanas(request, pais_id=None):
    if pais_id:
        pais =  models.Pais.objects.get(id =pais_id)
        query = models.Montana.objects.filter(pais=pais).order_by('-altitud')
        extension_titulo = f" en {pais.nombre}"
    else:
        query = models.Montana.objects.all().order_by('-altitud')
        extension_titulo = " "
    return render(request, "peak_wishlist/montanas.html", {'montanas': query, "extension_titulo": extension_titulo})

def  proyectos(request):
    query = models.Proyecto.objects.all().order_by('fecha_inicio')
    return render(request, "peak_wishlist/proyectos.html", {'proyectos': query})

def excursiones(rqequest, proyecto_id=None):
    if proyecto_id:
        proyecto =  models.Proyecto.objects.get(id =proyecto_id)
        query = models.Excursion.objects.filter(proyecto=proyecto).order_by('-fecha_hora_inicio')
        extension_titulo = f" de: {proyecto.nombre}"
    else:
        query = models.Excursion.objects.all().order_by('-fecha_hora_inicio')
        extension_titulo = ""
    return render(rqequest, 'peak_wishlist/excursiones.html', {'excursiones': query, "extension_titulo": extension_titulo})
    