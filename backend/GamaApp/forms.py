from django import forms
from GamaApp.models import *
from django.contrib.auth.forms import UserCreationForm
import os  # Asegúrate de importar el módulo os
import zipfile
from django.conf import settings
import json

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
            CustomUser.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                maternal_last_name=self.cleaned_data.get('maternal_last_name'),
                accepted_terms=self.cleaned_data['accepted_terms']
            )
        return user

class UploadProjectForm(forms.Form):
    name = forms.CharField(max_length=100, label="Nombre del Proyecto")
    description = forms.CharField(widget=forms.Textarea, label="Descripción del Proyecto", required=False)
    file = forms.FileField(label="Archivo ZIP")

    def save(self, user):
        project = Project.objects.create(name=self.cleaned_data['name'], description=self.cleaned_data['description'], owner=user.custom_profile)
        zip_file = self.cleaned_data['file']
        self.handle_uploaded_file(zip_file, project)
        return project

    def handle_uploaded_file(self, zip_file, project):
        project_dir = os.path.join(settings.MEDIA_ROOT, 'Projects', project.name)
        os.makedirs(project_dir, exist_ok=True)

        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(project_dir)

        models_dir = os.path.join(project_dir, 'models')
        for root, dirs, files in os.walk(models_dir):
            for file in files:
                if file.endswith('.gaml'):
                    gaml_file_path = os.path.join(root, file)
                    Simulation.objects.create(
                        name=os.path.basename(gaml_file_path).replace('.gaml', ''),
                        file=gaml_file_path,
                        project=project,
                        active=False
                    )

class SelectSimulationForm(forms.Form):
    selected_files = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=[],
        label="Selecciona los archivos .gaml que serán simulaciones"
    )
    active_files = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=[],
        label="Selecciona los archivos .gaml que estarán activos",
        required=False
    )

    def __init__(self, *args, **kwargs):
        gaml_files = kwargs.pop('gaml_files', [])
        super().__init__(*args, **kwargs)
        self.fields['selected_files'].choices = [(file, file) for file in gaml_files]
        self.fields['active_files'].choices = [(file, file) for file in gaml_files]

class ParameterForm(forms.Form):
    name = forms.CharField(max_length=100, label="Nombre del Parámetro")
    variable_name = forms.CharField(max_length=100, label="Nombre de la Variable")
    category = forms.CharField(max_length=100, label="Categoría", required=False)
    data_type = forms.ChoiceField(choices=[('float', 'Float'), ('boolean', 'Boolean')], label="Tipo de Dato")
    value = forms.CharField(max_length=100, label="Valor", required=False)
    min_value = forms.FloatField(label="Valor Mínimo", required=False)
    max_value = forms.FloatField(label="Valor Máximo", required=False)

class SelectParameterForm(forms.Form):
    parameters = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean_parameters(self):
        parameters = self.cleaned_data.get('parameters', '')
        if parameters:
            try:
                parameters = json.loads(parameters)
            except json.JSONDecodeError:
                raise forms.ValidationError("Formato de parámetros inválido.")
        return parameters