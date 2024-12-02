from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from django.views.generic import FormView
from GamaApp.forms import *
from GamaApp.models import Product
from django.urls import reverse_lazy
from django.contrib.auth import login as auth_login, logout as auth_logout

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
    context = {"lista":lista}
    return render(request, 'index.html',context)
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

def my_test_view(request, *args, **kwargs):
    print(args)
    print(kwargs)
    return HttpResponse("<h1>Hello World</h1>")

def login(request):
    return render(request, 'login.html')

def userview(request):
    return render(request, 'userview.html')

def simulation(request):
    return render(request, 'simulation.html')

def about(request):
    return render(request, 'about.html')

def faq(request):
    return render(request, 'faq.html')

class ProductFormView(generic.FormView):
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

def login(request):
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('login')