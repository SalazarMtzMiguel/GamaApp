from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from GamaApp.models import Simulation  # Cambia 'yourapp' por el nombre de tu app

# Crear grupos
superadmin_group, _ = Group.objects.get_or_create(name='Superadministradores')
admin_group, _ = Group.objects.get_or_create(name='Administradores')
user_group, _ = Group.objects.get_or_create(name='Usuarios')

# Asignar permisos personalizados
content_type = ContentType.objects.get_for_model(Simulation)

# Permisos para administradores
admin_permissions = [
    Permission.objects.get_or_create(codename='add_simulation', name='Can add simulation', content_type=content_type)[0],
    Permission.objects.get_or_create(codename='change_simulation', name='Can change simulation', content_type=content_type)[0],
]
admin_group.permissions.set(admin_permissions)

# Permisos para usuarios
user_permissions = [
    Permission.objects.get_or_create(codename='view_simulation', name='Can view simulation', content_type=content_type)[0],
]
user_group.permissions.set(user_permissions)
