from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, TemplateView
from django.views import generic
from django.urls import reverse_lazy
from GamaApp.forms import UserRegistrationForm, ProductForm
from GamaApp.models import Product

# Create your views here.

def my_view(request):
    lista=[
        {
            "title":"BMW"
        },{
            "title":"Mazda"
        },{
            "title":"Nissan"
        },
    ]
    context = {
        "lista": lista,
    }
    return render(request, 'index.html', context)

def lista(request):
    lista=[
        {"item":"item1"},
        {"item":"item2"},
        {"item":"item3"},
        {"item":"item4"},
        {"item":"item5"},
    ]
    context = {"lista":lista}
    return render(request, 'listado.html',context)

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

def about(request):
    return render(request, 'about.html')

def faq(request):
    return render(request, 'faq.html')

class ProductFormView(FormView):
    template_name = 'addproduct.html'
    form_class = ProductForm
    success_url = reverse_lazy('addproduct')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class ProductListView(generic.ListView):
    template_name = 'products.html'
    model = Product
    context_object_name = 'products'

class UserRegistrationView(FormView):
    template_name = 'register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)  # Inicia sesión automáticamente después del registro
        return redirect(self.success_url)

class AdminView(TemplateView):
    template_name = 'adminview.html'

class PermissionsView(TemplateView):
    template_name = 'permissions.html'