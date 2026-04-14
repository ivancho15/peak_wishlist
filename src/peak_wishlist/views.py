from django.shortcuts import render
from peak_wishlist import models

def index(request):
    return render(request, 'peak_wishlist/index.html')

def paises(request):
    query = models.Pais.objects.all()
    return render(request, "peak_wishlist/pais.html", {'paises': query})

def montanas(request):
    query = models.Montana.objects.all()
    return render(request, "peak_wishlist/montana.html", {'montanas': query})