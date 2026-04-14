from django.shortcuts import render
from peak_wishlist import models

def index(request):
    return render(request, 'peak_whishlist/index.html')

