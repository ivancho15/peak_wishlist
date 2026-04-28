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
    informacion_general = models.TextField(max_length=250, null=True, blank=True)
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
    informacion_general = models.TextField(max_length=250, null=True, blank=True)
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
    class DificultadEscalada(models.TextChoices):
        # Formato: 5.X - Y - Style
        R_56_4C_TRAD = "5.6 - 4c - Trad", "5.6 - 4c - Trad"
        R_56_4C_SPORT = "5.6 - 4c - Sport", "5.6 - 4c - Sport"
        R_57_5A_TRAD = "5.7 - 5a - Trad", "5.7 - 5a - Trad"
        R_57_5A_SPORT = "5.7 - 5a - Sport", "5.7 - 5a - Sport"
        R_58_5B_TRAD = "5.8 - 5b - Trad", "5.8 - 5b - Trad"
        R_58_5B_SPORT = "5.8 - 5b - Sport", "5.8 - 5b - Sport"
        R_59_5C_TRAD = "5.9 - 5c - Trad", "5.9 - 5c - Trad"
        R_59_5C_SPORT = "5.9 - 5c - Sport", "5.9 - 5c - Sport"
        R_510A_6A_TRAD = "5.10a - 6a - Trad", "5.10a - 6a - Trad"
        R_510A_6A_SPORT = "5.10a - 6a - Sport", "5.10a - 6a - Sport"
        R_510B_6A1_TRAD = "5.10b - 6a+ - Trad", "5.10b - 6a+ - Trad"
        R_510B_6A1_SPORT = "5.10b - 6a+ - Sport", "5.10b - 6a+ - Sport"
        R_510C_6B_TRAD = "5.10c - 6b - Trad", "5.10c - 6b - Trad"
        R_510C_6B_SPORT = "5.10c - 6b - Sport", "5.10c - 6b - Sport"
        R_510D_6B1_TRAD = "5.10d - 6b+ - Trad", "5.10d - 6b+ - Trad"
        R_510D_6B1_SPORT = "5.10d - 6b+ - Sport", "5.10d - 6b+ - Sport"
        R_511A_6C_TRAD = "5.11a - 6c - Trad", "5.11a - 6c - Trad"
        R_511A_6C_SPORT = "5.11a - 6c - Sport", "5.11a - 6c - Sport"
        R_511B_6C1_TRAD = "5.11b - 6c+ - Trad", "5.11b - 6c+ - Trad"
        R_511B_6C1_SPORT = "5.11b - 6c+ - Sport", "5.11b - 6c+ - Sport"
        R_511C_7A_TRAD = "5.11c - 7a - Trad", "5.11c - 7a - Trad"
        R_511C_7A_SPORT = "5.11c - 7a - Sport", "5.11c - 7a - Sport"
        R_511D_7A1_TRAD = "5.11d - 7a+ - Trad", "5.11d - 7a+ - Trad"
        R_511D_7A1_SPORT = "5.11d - 7a+ - Sport", "5.11d - 7a+ - Sport"
        R_512A_7B_TRAD = "5.12a - 7b - Trad", "5.12a - 7b - Trad"
        R_512A_7B_SPORT = "5.12a - 7b - Sport", "5.12a - 7b - Sport"
        R_512B_7B1_TRAD = "5.12b - 7b+ - Trad", "5.12b - 7b+ - Trad"
        R_513A_8A_SPORT = "5.13a - 8a - Sport", "5.13a - 8a - Sport"
        R_514A_8C_SPORT = "5.14a - 8c - Sport", "5.14a - 8c - Sport"
        R_515A_9B_SPORT = "5.15a - 9b - Sport", "5.15a - 9b - Sport"

    class DificultadAltaMontana(models.TextChoices):
        F = "F, I/II, 30°", "F, I/II, 30°"
        PD_MINUS = "PD-, II, 35°", "PD-, II, 35°"
        PD = "PD, II+, 40°", "PD, II+, 40°"
        PD_PLUS = "PD+, III, 45°", "PD+, III, 45°"
        AD_MINUS = "AD-, III+, 45°", "AD-, III+, 45°"
        AD = "AD, IV, 50°", "AD, IV, 50°"
        AD_PLUS = "AD+, IV+, 55°", "AD+, IV+, 55°"
        D_MINUS = "D-, V-, 60°", "D-, V-, 60°"
        D = "D, V, 65°", "D, V, 65°"
        D_PLUS = "D+, V+, 70°", "D+, V+, 70°"
        TD_MINUS = "TD-, VI-, 75°", "TD-, VI-, 75°"
        TD = "TD, VI, 80°", "TD, VI, 80°"
        TD_PLUS = "TD+, VI+, 85°", "TD+, VI+, 85°"
        ED1 = "ED1, VII, 90°", "ED1, VII, 90°"
        ED2 = "ED2, VII+, 90°", "ED2, VII+, 90°"
        ED3 = "ED3, VIII, 90°+", "ED3, VIII, 90°+"
        ED4 = "ED4, VIII+, 90°/100°", "ED4, VIII+, 90°/100°"

    class DificultadSenderismo(models.TextChoices):
        T1 = "T1, Senderismo", "T1, Senderismo"
        T2 = "T2, Senderismo de montaña", "T2, Senderismo de montaña"
        T3 = "T3, Senderismo de montaña exigente", "T3, Senderismo de montaña exigente"
        T4 = "T4, Senderismo alpino", "T4, Senderismo alpino"
        T5 = "T5, Senderismo alpino exigente", "T5, Senderismo alpino exigente"
        T6 = "T6, Senderismo alpino difícil", "T6, Senderismo alpino difícil"

    class DificultadMTB(models.TextChoices):
        S0 = "S0, Muy fácil", "S0, Muy fácil"
        S1 = "S1, Fácil", "S1, Fácil"
        S2 = "S2, Moderada", "S2, Moderada"
        S3 = "S3, Difícil", "S3, Difícil"
        S4 = "S4, Muy difícil", "S4, Muy difícil"
        S5 = "S5, Extrema", "S5, Extrema"
        
    
    class TipoActividad(models.TextChoices):
        ALTA_MONTANA = 'Alta Montaña'
        ESCALADA_EN_ROCA = 'Escalada'
        TREKKING = 'Trekking'
        MTB = 'Bicicleta de Montaña'

    class TipoTrayecto(models.TextChoices):
        IDA_Y_VUELTA = 'Ida y vuelta'
        Circuito = 'Circuito'
        Travesia = 'Travesia'
        Circunvalacion = 'Circunvalacion'

    class ExigenciaFisica(models.TextChoices):
        UN_DIA_E = 'Treking/escalada de un Dia'
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
    informacion_general = models.TextField(max_length=250, null=True, blank=True)
    gps_trakking = models.URLField(max_length=100, null=False, blank=False)
    montana = models.ForeignKey(Montana, null=False, blank= False, on_delete=models.CASCADE, verbose_name="montaña")
    equipo_sugerido = models.TextField(max_length=250, null=False, blank=False)
    tiempo_estimado = models.IntegerField(null=False, blank= False)
    unidad_tiempo_estimado = models.CharField(choices=UnidadTiempo.choices, blank=False, null=False)
    dificultad_tecnica = models.CharField(max_length=50, null=False, blank=False)
    observaciones = models.TextField(max_length=200, null=True, blank=True)
    indicaciones_inicio_ruta = models.TextField(max_length=200, null=True, blank=True)


    def __str__(self) -> str:
        return  f"{self.nombre} - {self.montana.nombre} - {self.tiempo_estimado} {self.unidad_tiempo_estimado} - {self.dificultad_tecnica}" 


#datos de proyecto
class Proyecto(models.Model):
    class Estado(models.TextChoices):
        PLANIFICADO = 'Planificado'
        COMPLETADO = 'Cumbre/Completado'
        
    nombre = models.CharField(max_length=250, null=False, blank=False)
    pais_destino = models.ForeignKey(Pais, on_delete=models.PROTECT, null=False, blank=False)
    fecha_inicio = models.DateField(null=False, blank=False)
    fecha_fin = models.DateField(null=False, blank=False)
    presupuesto_general = MoneyField(max_digits=8, decimal_places=0, null=False, blank=False)
    companeros = models.TextField(max_length=250, null=False, blank=False)
    estado = models.CharField(choices=Estado.choices, max_length=20, null=False, blank=True)

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