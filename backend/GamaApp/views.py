from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from GamaApp.mixins import SuperuserRequiredMixin, AdminOrSuperuserRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, TemplateView, UpdateView, DeleteView, ListView, View
from django.urls import reverse_lazy
from GamaApp.forms import UserRegistrationForm, UploadProjectForm,  SelectParameterForm, AssignProjectForm, AssignSimulationForm
from GamaApp.models import Project, Simulation, Parameter, UserProject, CustomUser, PublicSimulation
import os
from django.conf import settings
import zipfile
from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group


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
        user = self.request.user.custom_profile

        if self.request.user.is_superuser or self.request.user.groups.filter(name='Administradores').exists():
            # Superadministradores y administradores pueden ver todos los proyectos y simulaciones
            assigned_projects = Project.objects.all()
            public_simulations = Simulation.objects.filter(public_simulation__isnull=False, active=True)
        else:
            # Filtrar proyectos y simulaciones asignados al usuario
            assigned_projects = user.projects.all()
            public_simulations = Simulation.objects.filter(public_simulation__isnull=False, active=True)

        project_simulations = []
        for project in assigned_projects:
            active_simulations = project.simulations.filter(active=True)
            project_simulations.append({
                'project': project,
                'active_simulations': active_simulations
            })

        context['project_simulations'] = project_simulations
        context['public_simulations'] = public_simulations
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        if query:
            users = User.objects.filter(
                Q(username__icontains=query) |
                Q(email__icontains=query) |
                Q(custom_profile__first_name__icontains=query) |
                Q(custom_profile__last_name__icontains=query)
            )
        else:
            users = User.objects.all()

        for user in users:
            user.is_admin = user.groups.filter(name='Administradores').exists()

        context['users'] = users
        return context

class ConfirmAdminView(LoginRequiredMixin, SuperuserRequiredMixin, View):
    template_name = 'confirm_admin.html'

    def get(self, request, user_id, action):
        user = get_object_or_404(User, id=user_id)
        user.is_admin = user.groups.filter(name='Administradores').exists()
        return render(request, self.template_name, {'user': user, 'action': action})

    def post(self, request, user_id, action):
        user = get_object_or_404(User, id=user_id)
        admin_group = Group.objects.get(name='Administradores')
        if action == 'make_admin':
            user.groups.add(admin_group)
        elif action == 'revoke_admin':
            user.groups.remove(admin_group)
        user.save()
        return redirect('adminview')

class PermissionsView(LoginRequiredMixin, AdminOrSuperuserRequiredMixin, TemplateView):
    template_name = 'permissions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = CustomUser.objects.all()
        context['projects'] = Project.objects.all()  # Asegúrate de pasar los proyectos al contexto
        return context

class AddSimulationView(LoginRequiredMixin, AdminOrSuperuserRequiredMixin, TemplateView):
    template_name = 'add_simulation.html'

class EditSimulationParametersView(LoginRequiredMixin, AdminOrSuperuserRequiredMixin, View):
    template_name = 'edit_simulation_parameters.html'

    def get(self, request, user_id, simulation_id):
        user = get_object_or_404(CustomUser, id=user_id)
        simulation = get_object_or_404(Simulation, id=simulation_id)
        active_parameters = simulation.parameters.filter(active=True)
        inactive_parameters = simulation.parameters.filter(active=False)
        return render(request, self.template_name, {
            'user': user,
            'simulation': simulation,
            'active_parameters': active_parameters,
            'inactive_parameters': inactive_parameters
        })

    def post(self, request, user_id, simulation_id):
        user = get_object_or_404(CustomUser, id=user_id)
        simulation = get_object_or_404(Simulation, id=simulation_id)
        parameter_id = request.POST.get('parameter_id')
        action = request.POST.get('action')
        parameter = get_object_or_404(Parameter, id=parameter_id)

        if action == 'activate':
            parameter.active = True
        elif action == 'deactivate':
            parameter.active = False
        parameter.save()

        return redirect('edit_simulation_parameters', user_id=user_id, simulation_id=simulation_id)

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
            try:
                shutil.rmtree(project_dir)
                print(f"Directorio {project_dir} eliminado correctamente.")
            except Exception as e:
                print(f"Error al eliminar el directorio {project_dir}: {e}")
        return super().delete(request, *args, **kwargs)

class ProjectListForSimulationView(LoginRequiredMixin, AdminOrSuperuserRequiredMixin, ListView):
    model = Project
    template_name = 'project_list_for_simulation.html'
    context_object_name = 'projects'

class SelectSimulationView(LoginRequiredMixin, AdminOrSuperuserRequiredMixin, View):
    template_name = 'select_simulation.html'

    def get(self, request, project_id):
        project = Project.objects.get(id=project_id)
        simulations = project.simulations.filter(active=False)
        return render(request, self.template_name, {'project': project, 'simulations': simulations})

    def post(self, request, project_id):
        simulation_id = request.POST.get('simulation_id')
        simulation = get_object_or_404(Simulation, id=simulation_id)
        simulation.active = True
        simulation.save()
        return redirect('select_parameters', simulation_id=simulation.id)

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


class SelectParameterView(LoginRequiredMixin, AdminOrSuperuserRequiredMixin, View):
    template_name = 'select_parameters.html'

    def get(self, request, simulation_id):
        simulation = get_object_or_404(Simulation, id=simulation_id)
        form = SelectParameterForm()
        return render(request, self.template_name, {'simulation': simulation, 'form': form})

    def post(self, request, simulation_id):
        simulation = get_object_or_404(Simulation, id=simulation_id)
        form = SelectParameterForm(request.POST)
        if form.is_valid():
            parameters = form.cleaned_data['parameters']
            if parameters:
                for param in parameters:
                    Parameter.objects.create(
                        name=param['name'],
                        variable_name=param['variable_name'],
                        category=param.get('category', ''),
                        data_type=param['data_type'],
                        value=param.get('value', ''),
                        min_value=param.get('min_value', None),
                        max_value=param.get('max_value', None),
                        simulation=simulation
                    )
            return redirect('simulations')
        return render(request, self.template_name, {'simulation': simulation, 'form': form})

class ConfirmDeleteUserView(LoginRequiredMixin, SuperuserRequiredMixin, View):
    template_name = 'confirm_delete_user.html'

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        return render(request, self.template_name, {'user': user})

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return redirect('adminview')
    
class AssignProjectView(LoginRequiredMixin, AdminOrSuperuserRequiredMixin, View):
    template_name = 'assign_project.html'
    form_class = AssignProjectForm

    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        all_projects = Project.objects.all()
        user_projects = user.projects.all()
        available_projects = all_projects.difference(user_projects)
        return render(request, self.template_name, {
            'user': user,
            'available_projects': available_projects,
            'user_projects': user_projects
        })

    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        project_id = request.POST.get('project_id')
        action = request.POST.get('action')
        project = get_object_or_404(Project, id=project_id)

        if action == 'add':
            UserProject.objects.create(user=user, project=project, can_change_parameters=True)
            simulations = project.simulations.filter(active=True)
            for simulation in simulations:
                simulation.users_with_access.add(user)
        elif action == 'remove':
            UserProject.objects.filter(user=user, project=project).delete()
            simulations = project.simulations.filter(active=True)
            for simulation in simulations:
                simulation.users_with_access.remove(user)

        return redirect('permissions')

class AssignSimulationView(LoginRequiredMixin, AdminOrSuperuserRequiredMixin, View):
    template_name = 'assign_simulation.html'

    def get(self, request, user_id, project_id):
        user = get_object_or_404(CustomUser, id=user_id)
        project = get_object_or_404(Project, id=project_id)
        all_simulations = project.simulations.filter(active=True)
        assigned_simulations = all_simulations.filter(users_with_access=user)
        unassigned_simulations = all_simulations.difference(assigned_simulations)
        return render(request, self.template_name, {
            'user': user,
            'project': project,
            'assigned_simulations': assigned_simulations,
            'unassigned_simulations': unassigned_simulations
        })

    def post(self, request, user_id, project_id):
        user = get_object_or_404(CustomUser, id=user_id)
        project = get_object_or_404(Project, id=project_id)
        simulation_id = request.POST.get('simulation_id')
        action = request.POST.get('action')
        simulation = get_object_or_404(Simulation, id=simulation_id)

        if action == 'assign':
            simulation.users_with_access.add(user)
        elif action == 'remove':
            simulation.users_with_access.remove(user)

        return redirect('assign_simulation', user_id=user_id, project_id=project_id)
    
class ProjectSimulationListView(LoginRequiredMixin, AdminOrSuperuserRequiredMixin, TemplateView):
    template_name = 'project_simulation_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = Project.objects.all()
        project_simulations = []
        for project in projects:
            active_simulations = project.simulations.filter(active=True)
            project_simulations.append({
                'project': project,
                'active_simulations': active_simulations
            })
        context['project_simulations'] = project_simulations
        return context

    def post(self, request, *args, **kwargs):
        simulation_id = request.POST.get('simulation_id')
        action = request.POST.get('action')
        simulation = get_object_or_404(Simulation, id=simulation_id)

        if action == 'delete':
            simulation.active = False
            simulation.save()
            # Eliminar de simulaciones públicas si está presente
            PublicSimulation.objects.filter(simulation=simulation).delete()
        elif action == 'make_public':
            PublicSimulation.objects.get_or_create(simulation=simulation)
        elif action == 'remove_public':
            PublicSimulation.objects.filter(simulation=simulation).delete()

        return redirect('project_simulation_list')

class EditSimulationView(LoginRequiredMixin, AdminOrSuperuserRequiredMixin, View):
    template_name = 'edit_simulation.html'

    def get(self, request, simulation_id):
        simulation = get_object_or_404(Simulation, id=simulation_id)
        parameters = simulation.parameters.all()
        return render(request, self.template_name, {
            'simulation': simulation,
            'parameters': parameters
        })

    def post(self, request, simulation_id):
        simulation = get_object_or_404(Simulation, id=simulation_id)
        action = request.POST.get('action')
        if action == 'delete':
            simulation.active = False
            simulation.save()
            return redirect('project_simulation_list')
        elif action == 'update':
            parameter_id = request.POST.get('parameter_id')
            parameter = get_object_or_404(Parameter, id=parameter_id)
            parameter.name = request.POST.get('name')
            parameter.variable_name = request.POST.get('variable_name')
            parameter.category = request.POST.get('category')
            parameter.data_type = request.POST.get('data_type')
            parameter.value = request.POST.get('value')
            parameter.min_value = request.POST.get('min_value')
            parameter.max_value = request.POST.get('max_value')
            parameter.save()
            return redirect('edit_simulation', simulation_id=simulation_id)
        elif action == 'add':
            Parameter.objects.create(
                name=request.POST.get('name'),
                variable_name=request.POST.get('variable_name'),
                category=request.POST.get('category'),
                data_type=request.POST.get('data_type'),
                value=request.POST.get('value'),
                min_value=request.POST.get('min_value'),
                max_value=request.POST.get('max_value'),
                simulation=simulation
            )
            return redirect('edit_simulation', simulation_id=simulation_id)
        elif action == 'remove':
            parameter_id = request.POST.get('parameter_id')
            parameter = get_object_or_404(Parameter, id=parameter_id)
            parameter.delete()
            return redirect('edit_simulation', simulation_id=simulation_id)