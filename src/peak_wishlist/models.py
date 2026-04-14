from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from djmoney.models.fields import MoneyField

#modelo pais, define el pais donde se ubica la montaña o ruta
class Pais(models.Model):
    class Continente(models.TextChoices):
        AMERICA = 'America'
        EUROPA = 'Europa'
        AFRICA = 'Africa'
        OCEANIA = 'Oceania'
        ASIA = 'Asia'
    nombre = models.CharField(max_length= 50)
    continente = models.CharField(max_length=20, choices=Continente.choices, null=False)

    def __str__(self) -> str:
        return  f"{self.nombre}"
    
    class Meta:
        verbose_name="Pais"
        verbose_name_plural="Paises"

#modelo parque: datos de parque o zona protegida donde se ubica una montaña o ruta
class Parque(models.Model):
    class TipoParque(models.TextChoices):
        PRIVADO = 'Privado'
        PUBLICO = 'Publico'
    nombre = models.CharField(max_length=50, null=False, blank=False)
    tipo = models.CharField(max_length=8, choices=TipoParque.choices, null=False)
    correo = models.EmailField(null=True, blank=True, max_length=50)
    telefono = PhoneNumberField(null=True, blank=True)
    web_site = models.URLField(null=True, blank=True, max_length=60)
    pais = models.ForeignKey(Pais, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return  f"{self.nombre}"
    
    class Meta:
        verbose_name="Parque"
        verbose_name_plural="Parques"

#Datos de montaña
class Montana(models.Model):
    nombre = models.CharField(max_length= 50, null=False, blank=False)
    altitud = models.PositiveIntegerField(null=False, blank=False)
    cordillera = models.CharField(max_length=50, null=True, blank=True)
    pais = models.ManyToManyField(Pais, related_name="montanas")
    provincia_estado_departamento_region = models.CharField(max_length=50, blank=False)    
    requiere_permiso = models.BooleanField(default=False)
    parque = models.ForeignKey(Parque, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"{self.nombre} - {self.altitud} msnm - {self.cordillera}"

    class Meta:
        verbose_name="Montaña"
        verbose_name_plural="Montañas"

#datos de Refugios de montaña
class Refugio(models.Model):
    nombre = models.CharField(max_length= 50, null=False, blank=False)
    altitud = models.PositiveIntegerField(null=False, blank=False)
    capacidad = models.IntegerField(null=True, blank=True)
    servicios = models.TextField(max_length=250, null=True, blank=True)
    costo = MoneyField(max_digits=10, decimal_places=2, null=True, blank=True)
    telf_contacto = PhoneNumberField(null=True, blank=True)
    correo_contacto = models.EmailField(null=True, blank=True, max_length=50)
    montana = models.ForeignKey(Montana, null=False, blank= False, on_delete=models.CASCADE, verbose_name="montaña")
    
    def __str__(self) -> str:
        return  f"{self.nombre} - {self.montana.nombre}"
    
#datos de ruta de montaña
class Ruta(models.Model):
    class TipoActividad(models.TextChoices):
        ALTA_MONTANA = 'Alta Montaña'
        ESCALDA_EN_ROCA = 'Escalada'
        TREKKING = 'Trekking'
        MTB = 'Bicicleta de Montaña'

    class TipoTrayecto(models.TextChoices):
        IDA_Y_VUELTA = 'Ida y vuelta'
        Circuito = 'Circuito'
        Travesia = 'Travesia'
        Circunvalacion = 'Circunvalacion'

    class ExigenciaFisica(models.TextChoices):
        UN_DIA = 'Treking de un Dia'
        DOS_DIAS = 'Trekking/escalada de Fin de Semana'
        VARIOS_DIAS = 'Varios Dias en Montaña'
        GRAN_RECORRIDO = 'Gran Recorrido'
        RECORRIDO_LOCAL = 'Recorrido Local'

    class UnidadTiempo(models.TextChoices):
        DIAS = 'Dias'
        HORAS = 'Horas'

    nombre = models.CharField(max_length= 50, null=False, blank=False, default="Ruta Normal")
    actividad = models.CharField(max_length=30, choices=TipoActividad.choices, null=False, blank=False)
    tipo_trayecto = models.CharField(max_length=20, choices=TipoTrayecto.choices, null=False, blank=False)
    exigencia = models.CharField(max_length=50, choices=ExigenciaFisica.choices, null=False, blank=False)
    distancia = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    desnivel_positivo = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    gps_trakking = models.URLField(max_length=100, null=False, blank=False)
    montana = models.ForeignKey(Montana, null=False, blank= False, on_delete=models.CASCADE, verbose_name="montaña")
    equipo_sugerido = models.TextField(max_length=250, null=False, blank=False)
    tiempo_estimado = models.IntegerField(null=False, blank= False)
    unidad_tiempo_estimado = models.CharField(choices=UnidadTiempo.choices, blank=False, null=False)
    dificultad_tecnica = models.CharField(max_length=20, null=False, blank=False)
    observaciones = models.TextField(max_length=200, null=True, blank=True)
    indicaciones_inicio_ruta = models.TextField(max_length=200, null=True, blank=True)


    def __str__(self) -> str:
        return  f"{self.nombre} - {self.montana.nombre} - {self.tiempo_estimado} {self.unidad_tiempo_estimado} - {self.dificultad_tecnica}" 


#datos de proyecto
class Proyecto(models.Model):
    nombre = models.CharField(max_length=250, null=False, blank=False)
    pais_destino = models.ForeignKey(Pais, on_delete=models.PROTECT, null=False, blank=False)
    fecha_inicio = models.DateField(null=False, blank=False)
    fecha_fin = models.DateField(null=False, blank=False)
    presupuesto_general = MoneyField(max_digits=6, decimal_places=0, null=False, blank=False)
    companeros = models.TextField(max_length=250, null=False, blank=False)

    def __str__(self):
        return f"{self.nombre}: {self.fecha_inicio} - {self.fecha_fin}" 

#datos de salida/excursion
class Excursion(models.Model):
    class Modalidad(models.TextChoices):
        GUIADO = 'Guiado'
        AUTOGUIADO = 'Autoguiado'
    
    class Estado(models.TextChoices):
        PLANIFICADO = 'Planificado'
        CUMBRE_COMPLETADO = 'Cumbre/Completado'
        INTENTO = 'Intento'
        CANCELADO = 'Cancelado'

    fecha_hora_inicio = models.DateTimeField(blank=False, null=False)
    fecha_hora_fin = models.DateTimeField(blank=False, null=False)
    equipo_utilizado = models.TextField(max_length=250, null=False, blank=False)
    companeros = models.TextField(max_length=250, null=False, blank=False)
    condiciones = models.TextField(max_length=250, null=False, blank=False)
    observaciones = models.TextField(max_length=250, null=False, blank=False)
    costo_total = MoneyField(max_digits=10, decimal_places=2, null=True, blank=True)
    modalidad = models.CharField(choices=Modalidad.choices, max_length=15, null=False, blank=True)
    estado = models.CharField(choices=Estado.choices, max_length=20, null=False, blank=True)
    ruta = models.ForeignKey(Ruta, on_delete=models.PROTECT, null=False, blank=False, related_name='salidas')
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, null=True, blank=True, related_name='actividades')
    

    def __str__(self) -> str:
        return  f"{self.fecha_hora_inicio} - {self.fecha_hora_fin} - {self.ruta.montana} - {self.ruta.nombre} - {self.estado}"     

    class Meta:
        verbose_name="Excursion"
        verbose_name_plural="Excursiones"