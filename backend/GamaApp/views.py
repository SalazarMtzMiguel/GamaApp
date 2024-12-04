from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from GamaApp.mixins import SuperuserRequiredMixin, AdminOrSuperuserRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, TemplateView, UpdateView, DeleteView, ListView, View
from django.urls import reverse_lazy
from GamaApp.forms import UserRegistrationForm, UploadProjectForm, SelectSimulationForm
from GamaApp.models import Project, Simulation, Parameter
import os
from django.conf import settings
import zipfile
from django.http import HttpResponse

# Create your views here.

def my_view(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('simulations')
        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'login.html')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def userview(request):
    return render(request, 'userview.html')

class SimulationsView(LoginRequiredMixin, TemplateView):
    template_name = 'simulations.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        return context

def about(request):
    return render(request, 'about.html')

def faq(request):
    return render(request, 'faq.html')

class UserRegistrationView(FormView):
    template_name = 'register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)  # Inicia sesión automáticamente después del registro
        return redirect(self.success_url)

class AdminView(LoginRequiredMixin, SuperuserRequiredMixin, TemplateView):
    template_name = 'adminview.html'

class PermissionsView(LoginRequiredMixin, AdminOrSuperuserRequiredMixin, TemplateView):
    template_name = 'permissions.html'

class AddSimulationView(LoginRequiredMixin, AdminOrSuperuserRequiredMixin, TemplateView):
    template_name = 'add_simulation.html'

class EditSimulationView(LoginRequiredMixin, AdminOrSuperuserRequiredMixin, TemplateView):
    template_name = 'edit_simulation.html'

class DeleteSimulationView(LoginRequiredMixin, AdminOrSuperuserRequiredMixin, TemplateView):
    template_name = 'delete_simulation.html'

class AddProjectView(LoginRequiredMixin, AdminOrSuperuserRequiredMixin, FormView):
    template_name = 'add_project.html'
    form_class = UploadProjectForm
    success_url = reverse_lazy('simulations')

    def form_valid(self, form):
        form.save(self.request.user)
        return super().form_valid(form)

class EditProjectView(LoginRequiredMixin, AdminOrSuperuserRequiredMixin, UpdateView):
    model = Project
    fields = ['description']
    template_name = 'edit_project_detail.html'
    success_url = reverse_lazy('simulations')

class ProjectListView(LoginRequiredMixin, AdminOrSuperuserRequiredMixin, ListView):
    model = Project
    template_name = 'project_list.html'
    context_object_name = 'projects'

class DeleteProjectView(LoginRequiredMixin, AdminOrSuperuserRequiredMixin, DeleteView):
    model = Project
    template_name = 'confirm_delete_project.html'
    success_url = reverse_lazy('delete_project')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        project_dir = os.path.join(settings.MEDIA_ROOT, 'Projects', self.object.name)
        if os.path.exists(project_dir):
            import shutil
            shutil.rmtree(project_dir)
        return super().delete(request, *args, **kwargs)

class ProjectListForSimulationView(LoginRequiredMixin, AdminOrSuperuserRequiredMixin, ListView):
    model = Project
    template_name = 'project_list_for_simulation.html'
    context_object_name = 'projects'

class SelectSimulationView(LoginRequiredMixin, AdminOrSuperuserRequiredMixin, View):
    template_name = 'select_simulation.html'

    def get(self, request, project_id):
        project = Project.objects.get(id=project_id)
        project_dir = os.path.join(settings.MEDIA_ROOT, 'Projects', project.name, 'models')
        gaml_files = [f for f in os.listdir(project_dir) if f.endswith('.gaml')]
        return render(request, self.template_name, {'project': project, 'gaml_files': gaml_files})

    def post(self, request, project_id):
        project = Project.objects.get(id=project_id)
        selected_files = request.POST.getlist('selected_files')
        for file_name in selected_files:
            gaml_file_path = os.path.join(settings.MEDIA_ROOT, 'Projects', project.name, 'models', file_name)
            self.read_gaml_file(gaml_file_path, project)
        return redirect('simulations')

    def read_gaml_file(self, gaml_file_path, project):
        with open(gaml_file_path, 'r') as file:
            simulation_name = os.path.basename(gaml_file_path).replace('.gaml', '')
            simulation = Simulation.objects.create(name=simulation_name, file=gaml_file_path, project=project, active=False)
            for line in file:
                if line.startswith('parameter'):
                    parts = line.split()
                    name = parts[1]
                    description = ' '.join(parts[2:])
                    Parameter.objects.create(name=name, description=description, simulation=simulation)

class ProcessSimulationView(LoginRequiredMixin, AdminOrSuperuserRequiredMixin, View):
    def post(self, request, project_id):
        project = Project.objects.get(id=project_id)
        selected_files = request.POST.getlist('selected_files')
        for file_name in selected_files:
            gaml_file_path = os.path.join(settings.MEDIA_ROOT, 'Projects', project.name, 'models', file_name)
            self.read_gaml_file(gaml_file_path, project)
        return redirect('simulations')

    def read_gaml_file(self, gaml_file_path, project):
        with open(gaml_file_path, 'r') as file:
            simulation_name = os.path.basename(gaml_file_path).replace('.gaml', '')
            simulation = Simulation.objects.create(name=simulation_name, file=gaml_file_path, project=project, active=False)
            for line in file:
                if line.startswith('parameter'):
                    parts = line.split()
                    name = parts[1]
                    description = ' '.join(parts[2:])
                    Parameter.objects.create(name=name, description=description, simulation=simulation)

@login_required
def run_simulation(request, simulation_id):
    simulation = get_object_or_404(Simulation, id=simulation_id)
    # Aquí puedes añadir el código para ejecutar la simulación
    return HttpResponse(f"Ejecutando simulación: {simulation.name}")