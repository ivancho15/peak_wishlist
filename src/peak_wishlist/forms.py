from django import forms
from peak_wishlist.models import Montana, Excursion, Refugio, Ruta, Parque, Proyecto
from django.urls import reverse_lazy

class MontanaForm(forms.ModelForm):
    class Meta:
        model = Montana
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control rounded-4', 'rows': '3'})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control rounded-pill'})

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

class RefugioForm(forms.ModelForm):
    class Meta:
        model = Refugio
        fields = ['nombre', 'altitud', 'capacidad', 'servicios', 'costo', 'telf_contacto', 'correo_contacto']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control rounded-4', 'rows': '3'})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control rounded-pill'})

class RutaForm(forms.ModelForm):
    class Meta:
        model = Ruta
        exclude = ['montana'] 
        widgets = {
            'dificultad_tecnica': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'actividad' in self.fields:
            self.fields['actividad'].widget.attrs.update({
                'hx-get': reverse_lazy('peak_wishlist:opciones_dificultades'),
                'hx-target': '#id_dificultad_tecnica', 
                'hx-trigger': 'change',
            })

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control rounded-4', 'rows': '3'})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control rounded-pill'})

class ParqueForm(forms.ModelForm):
    class Meta:
        model = Parque
        exclude = ['pais'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control rounded-4', 'rows': '3'})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control rounded-pill'})


class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = "__all__"

class ExursionForm(forms.ModelForm):
    class Meta:
        model = Excursion
        fields = "__all__"