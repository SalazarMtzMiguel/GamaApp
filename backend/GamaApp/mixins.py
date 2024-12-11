from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from GamaApp.models import Simulation

class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class AdminOrSuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='Administradores').exists()

class UserHasSimulationAccessMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Administradores').exists():
            return True
        simulation_id = self.kwargs['simulation_id']
        simulation = get_object_or_404(Simulation, id=simulation_id)
        return simulation.project.assigned_users.filter(id=self.request.user.custom_profile.id).exists()