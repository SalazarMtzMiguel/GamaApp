from django.db import models
from django.contrib.auth.models import User

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='custom_profile')
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    maternal_last_name = models.CharField(max_length=150, blank=True, null=True)
    accepted_terms = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects')
    file = models.FileField(upload_to='Projects/')

    def __str__(self):
        return self.name

class Simulation(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='Projects/%Y/%m/%d/')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='simulations')
    users_with_access = models.ManyToManyField(CustomUser, related_name='allowed_simulations')
    active = models.BooleanField(default=False)  # Campo para indicar si la simulación está activa

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(CustomUser, related_name='roles')

    def __str__(self):
        return self.name

class Parameter(models.Model):
    name = models.CharField(max_length=100,default='Parametros')
    variable_name = models.CharField(max_length=100,default='variable')
    category = models.CharField(max_length=100, blank=True, null=True)
    data_type = models.CharField(max_length=50,default='int')
    value = models.CharField(max_length=100, blank=True, null=True)
    min_value = models.FloatField(blank=True, null=True)
    max_value = models.FloatField(blank=True, null=True)
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE, related_name='parameters')

    def __str__(self):
        return self.name

class RoleParameter(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_parameters')
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, related_name='role_parameters')
    can_control = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.role.name} - {self.parameter.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username