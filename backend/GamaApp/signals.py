from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, User
from django.dispatch import receiver

@receiver(post_migrate)
def create_default_groups_and_users(sender, **kwargs):
    if sender.name == 'GamaApp':
        # Crear grupos predeterminados
        admin_group, _ = Group.objects.get_or_create(name='Administradores')
        user_group, _ = Group.objects.get_or_create(name='Usuarios')

        # Crear superadministrador
        if not User.objects.filter(username='CINVESTAV').exists():
            superadmin = User.objects.create_superuser(
                username='CINVESTAV',
                email='superadmin@cinvestav.mx',  # Se puede ajustar según sea necesario
                password='CINVES2024'
            )
            superadmin.groups.add(admin_group)
            print("Superadministrador creado: CINVESTAV")

        # Crear un administrador básico
        if not User.objects.filter(username='admin1').exists():
            admin_user = User.objects.create_user(
                username='admin1',
                email='admin1@domain.com',
                password='admin123'
            )
            admin_user.groups.add(admin_group)
            print("Administrador básico creado: admin1")

        # Crear un usuario regular
        if not User.objects.filter(username='user1').exists():
            user = User.objects.create_user(
                username='user1',
                email='user1@domain.com',
                password='user123'
            )
            user.groups.add(user_group)
            print("Usuario básico creado: user1")