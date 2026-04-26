from django.shortcuts import render
from peak_wishlist import models

def index(request):
    return render(request, 'peak_wishlist/index.html')


def paises(request):
    query = models.Pais.objects.all().order_by('nombre')
    return render(request, "peak_wishlist/paises.html", {'paises': query})


def  parques(request, pais_id=None):
    pais = models.Pais.objects.get(id=pais_id)
    query = models.Parque.objects.filter(pais=pais).order_by('nombre')
    extension_titulo = f"en {pais.nombre}"
    contexto = {'parques': query, 'extension_titulo':  extension_titulo}
    return render(request, "peak_wishlist/parques.html", contexto)

def montanas(request, pais_id=None, parque_id=None):
    if pais_id:
        pais =  models.Pais.objects.get(id =pais_id)
        query = models.Montana.objects.filter(pais=pais).order_by('-altitud')
        extension_titulo = f" en {pais.nombre}"
    elif parque_id:
        parque =  models.Parque.objects.get(id =parque_id)
        query = models.Montana.objects.filter(parque=parque).order_by('-altitud')
        extension_titulo = f" en {parque.nombre} ({ parque.pais })"
    else:
        query = models.Montana.objects.all().order_by('-altitud')
        extension_titulo = " "
    return render(request, "peak_wishlist/montanas.html", {'montanas': query, "extension_titulo": extension_titulo})

def  proyectos(request):
    query = models.Proyecto.objects.all().order_by('fecha_inicio')
    return render(request, "peak_wishlist/proyectos.html", {'proyectos': query})

def excursiones(rqequest, proyecto_id=None, ruta_id=None, montana_id=None):
    if proyecto_id:
        proyecto =  models.Proyecto.objects.get(id =proyecto_id)
        query = models.Excursion.objects.filter(proyecto=proyecto).order_by('-fecha_hora_inicio')
        extension_titulo = f" de: {proyecto.nombre}"
    elif  ruta_id:
        ruta =  models.Ruta.objects.get(id =ruta_id)
        query = models.Excursion.objects.filter(ruta=ruta).order_by('-fecha_hora_inicio')
        extension_titulo = f" en: {ruta.nombre} de {ruta.montana.nombre}"
    elif  montana_id:
        montana =  models.Montana.objects.get(id =montana_id)
        query = models.Excursion.objects.filter(ruta__montana=montana).order_by('-fecha_hora_inicio')
        extension_titulo = f" en: {montana.nombre} "
    else:
        query = models.Excursion.objects.all().order_by('-fecha_hora_inicio')
        extension_titulo = ""
    return render(rqequest, 'peak_wishlist/excursiones.html', {'excursiones': query, "extension_titulo": extension_titulo})


def rutas(request, montana_id=None):
    montana = models.Montana.objects.get(id = montana_id)
    query = models.Ruta.objects.filter(montana = montana)
    extension_titulo = f"en {montana.nombre}"
    contexto = {'rutas': query, 'extension_titulo': extension_titulo}
    return render(request, 'peak_wishlist/rutas.html', contexto)

def refugios(request, montana_id=None):
    montana = models.Montana.objects.get(id = montana_id)
    query = models.Refugio.objects.filter(montana = montana)
    extension_titulo = f"{montana.nombre}"
    contexto = {'refugios': query, 'extension_titulo': extension_titulo}
    return render(request, 'peak_wishlist/refugios.html', contexto)