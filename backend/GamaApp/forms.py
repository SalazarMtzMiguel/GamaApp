from django import forms
from GamaApp.models import *
from django.contrib.auth.forms import UserCreationForm


class ProductForm(forms.Form):
    name = forms.CharField(
        max_length=200,
        label="Nombre",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'})
    )
    description = forms.CharField(
        max_length=500,
        label="Descripción",
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del producto', 'rows': 3})
    )
    price = forms.FloatField(
        label="Precio",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio en MXN'})
    )
    available = forms.BooleanField(
        initial=True,
        label="Disponible",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    photo = forms.ImageField(
        label="Foto",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    def save(self):
        Product.objects.create(
            name=self.cleaned_data['name'],
            description=self.cleaned_data['description'],
            price=self.cleaned_data['price'],
            available=self.cleaned_data['available'],
            photo=self.cleaned_data['photo']
        )

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label="Nombre de usuario", max_length=150)
    first_name = forms.CharField(label="Nombre(s)", max_length=150)
    last_name = forms.CharField(label="Apellido paterno", max_length=150)
    maternal_last_name = forms.CharField(label="Apellido materno", max_length=150, required=False)
    email = forms.EmailField(label="Correo electrónico")
    accepted_terms = forms.BooleanField(label="Acepto los términos y condiciones", required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Crear el perfil de usuario relacionado
            CustomUser.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                maternal_last_name=self.cleaned_data.get('maternal_last_name'),
                accepted_terms=self.cleaned_data['accepted_terms']
            )
        return user