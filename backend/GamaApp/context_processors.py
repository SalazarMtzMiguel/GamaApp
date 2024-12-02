from django.contrib.auth.models import Group

def user_roles(request):
    return {
        "is_superuser": request.user.is_superuser,
        "is_admin": request.user.groups.filter(name='Administradores').exists() if request.user.is_authenticated else False,
        "is_user": request.user.groups.filter(name='Usuarios').exists() if request.user.is_authenticated else False,
    }