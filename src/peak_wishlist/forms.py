from django import forms
from peak_wishlist.models import Montana, Excursion, Refugio, Ruta, Parque, Proyecto
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError

#Formulario Montaña
class MontanaForm(forms.ModelForm):
    class Meta:
        model = Montana
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #da estilos a los fields del formulari
        dar_estilo(self, self.fields)

    def clean(self):
        cleaned_data = super().clean()
        paises_seleccionados = cleaned_data.get("pais")
        parque = cleaned_data.get("parque")

        if parque and paises_seleccionados:
            if not paises_seleccionados.filter(id=parque.pais.id).exists():
                nombres_paises = ", ".join([p.nombre for p in paises_seleccionados])
                raise forms.ValidationError(
                    f"El parque '{parque.nombre}' pertenece a {parque.pais.nombre}, "
                    f"pero has seleccionado: {nombres_paises}. ¡La brújula no coincide!")
        return cleaned_data

#Formulario Refugio
class RefugioForm(forms.ModelForm):
    class Meta:
        model = Refugio
        fields = ['nombre', 'altitud', 'capacidad', 'servicios', 'costo', 'telf_contacto', 'correo_contacto']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #da estilos a los fields del formulario
        dar_estilo(self, self.fields)

#Formulario Ruta
class RutaForm(forms.ModelForm):
    class Meta:
        model = Ruta
        exclude = ['montana'] 
        widgets = {
            'dificultad_tecnica': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control rounded-4', 'rows': '3'})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control rounded-pill'})

        #Filtra el dropdown de dificultat tecnica segun la actividad
        if 'actividad' in self.fields:
            self.fields['actividad'].widget.attrs.update({
                'hx-get': reverse_lazy('peak_wishlist:opciones_dificultades'),
                'hx-target': '#id_dificultad_tecnica', 
                'hx-trigger': 'change',
            })

        #da estilos a los fields del formulario
        dar_estilo(self, self.fields)

#Formulario Parque
class ParqueForm(forms.ModelForm):
    class Meta:
        model = Parque
        exclude = ['pais'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #da estilos a los fields del formulario
        dar_estilo(self, self.fields)

#Formulario proyecto
class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = "__all__"
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #da estilos a los fields del formulario
        dar_estilo(self, self.fields)

#formualrio excursion 
class ExursionForm(forms.ModelForm):
    class Meta:
            model = Excursion
            fields = "__all__"
            widgets = {
                'fecha_hora_inicio': forms.DateTimeInput(
                        attrs={'type': 'datetime-local', 'class': 'form-control rounded-pill'},
                        format='%Y-%m-%dT%H:%M'
                    ),
                'fecha_hora_fin': forms.DateTimeInput(
                        attrs={'type': 'datetime-local', 'class': 'form-control rounded-pill'},
                        format='%Y-%m-%dT%H:%M'
                    ),
                'equipo_utilizado': forms.Textarea(attrs={'rows': 3, 'class': 'form-control rounded-4'}),
                'condiciones': forms.Textarea(attrs={'rows': 2, 'class': 'form-control rounded-4'}),
                'observaciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control rounded-4'}),
                'companeros': forms.Textarea(attrs={'rows': 2, 'class': 'form-control rounded-4'}),
            }

    def __init__(self, *args, **kwargs):
        
        m_id = kwargs.pop('m_id', None)
        p_id = kwargs.pop('p_id', None)
        r_id = kwargs.pop('r_id', None)
        
        super().__init__(*args, **kwargs)

        #da estilos a los fields del formulario
        dar_estilo(self, self.fields)

        #fFiltra proyectos, solo proyectos no completados se le spuede añadir excursiones
        self.fields['proyecto'].queryset = Proyecto.objects.exclude(estado='Cumbre/Completado') #type: ignore
 
        """
        Deshabilita la edicion de proyecto y ruta, esto
        pobla los campos de fecha
        """
        if self.instance.pk:
            if self.instance.fecha_hora_inicio:
                self.fields['fecha_hora_inicio'].initial = self.instance.fecha_hora_inicio.strftime('%Y-%m-%dT%H:%M')
            if self.instance.fecha_hora_fin:
                self.fields['fecha_hora_fin'].initial = self.instance.fecha_hora_fin.strftime('%Y-%m-%dT%H:%M')
            
            self.fields['proyecto'].disabled = True
            if self.instance.proyecto:
                self.fields['proyecto'].queryset = Proyecto.objects.filter(id=self.instance.proyecto.id) #type: ignore
            
            self.fields['ruta'].disabled = True
            self.fields['ruta'].queryset = Ruta.objects.filter(id=self.instance.ruta.id) #type: ignore

        else:
            # Comportamiento cuando se invoca el formulario desde Proyecto
            if p_id or (self.instance.pk and self.instance.proyecto):
                #preselecciona el proyecto
                actual_p_id = p_id or self.instance.proyecto.id
                self.fields['proyecto'].disabled = True
                self.fields['proyecto'].initial = actual_p_id 

                # Filtro rutas: que pertenezcan a montañas del mismo país que el proyecto
                proyecto = Proyecto.objects.get(id=actual_p_id)
                self.fields['ruta'].queryset = Ruta.objects.filter( #type: ignore
                    montana__pais=proyecto.pais_destino
                ).order_by('montana__nombre', 'nombre')

            # Comportamiento cuando se invoca desde Montaña
            elif m_id or (self.instance.pk and self.instance.ruta):
                
                # Filtro: Solo rutas de esta montaña específica
                actual_m_id = m_id or self.instance.ruta.montana.id
                self.fields['ruta'].queryset = Ruta.objects.filter(montana_id=actual_m_id).order_by('nombre')  #type: ignore
            
            # Comportamiento  cuando se invoca desde Ruta
            elif r_id or (self.instance.pk and self.instance.ruta):
                
                #presellecciona la ruta
                actual_r_id = r_id or self.instance.ruta.id
                self.fields['ruta'].initial = actual_r_id 
                self.fields['ruta'].disabled = True

            # Listado General (sin parámetros)
            else:
                # Ordenado por montaña 
                self.fields['ruta'].queryset = Ruta.objects.all().order_by('montana__nombre', 'nombre')  #type: ignore


    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get("fecha_hora_inicio")
        fecha_fin = cleaned_data.get("fecha_hora_fin")

        #validacion fecha
        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            raise ValidationError({  
                'fecha_hora_fin': "La fecha de finalización no puede ser anterior a la fecha de inicio."
            })
        return cleaned_data
    

def dar_estilo(self, fields: dict):
        
    for name, field in self.fields.items():
        if isinstance(field.widget, forms.Textarea):
            field.widget.attrs.update({'class': 'form-control rounded-4', 'rows': '3'})
        elif isinstance(field.widget, forms.CheckboxInput):
            field.widget.attrs.update({'class': 'form-check-input'})
        else:
            field.widget.attrs.update({'class': 'form-control rounded-pill'})

            