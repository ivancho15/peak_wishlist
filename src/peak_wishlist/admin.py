from django.contrib import admin
from peak_wishlist import models
 
@admin.register(models.Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ("nombre", "continente")
    search_fields = ('nombre', 'continente')
    ordering = ('nombre', 'continente')

@admin.register(models.Parque)
class ParqueAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pais')
    search_fields = ('nombre', 'pais__nombre')
    ordering = ('nombre', 'pais')
    list_filter = ('pais',)

@admin.register(models.Montana)
class MontanaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'altitud', 'pais')
    search_fields = ('nombre', 'pais__nombre', 'cordillera', 'parque__nombre')
    list_filter = ('pais', 'cordillera', 'requiere_permiso')
    ordering = ('nombre', 'altitud')

@admin.register(models.Refugio)
class RefugioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'montana')
    search_fields = ('nombre', 'montana__nombre')
    list_filter = ('montana',)
    ordering = ('nombre', 'montana__nombre', 'costo')

@admin.register(models.Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'montana', 'actividad', 'dificultad_tecnica', 'tipo_trayecto')
    search_fields = ('nombre', 'montana__nombre', 'actividad')
    list_filter = ('montana', 'actividad', 'dificultad_tecnica', 'tipo_trayecto', 'exigencia' )
    ordering = ('montana','actividad', 'dificultad_tecnica', 'tipo_trayecto', 'exigencia', )

@admin.register(models.Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pais_destino', 'fecha_inicio')
    search_fields = ('nombre', 'pais_destino__nombre')
    list_filter = ('pais_destino',) 
    ordering = ('pais_destino', '-fecha_inicio')
    date_hierarchy = 'fecha_inicio'

@admin.register(models.Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('fecha_hora_inicio', 'ruta', 'estado')
    search_fields = ('ruta__montana__pais__nombre','ruta__montana__nombre','ruta__nombre', 'proyecto__nombre')
    list_filter = ('ruta', 'proyecto', 'estado')
    ordering = ('-fecha_hora_inicio', 'estado')
    date_hierarchy = 'fecha_hora_inicio'



    