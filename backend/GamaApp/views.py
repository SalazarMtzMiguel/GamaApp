from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from GamaApp.forms import ProductForm 
from GamaApp.models import Product
from django.urls import reverse_lazy

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

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

def userview(request):
    return render(request, 'userview.html')

def simulation(request):
    return render(request, 'simulation.html')



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