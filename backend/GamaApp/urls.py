"""
URL configuration for GamaBackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from GamaApp.views import *


urlpatterns = [
    path('', my_view, name='index'),
    path('test/', my_test_view, name='test'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('userview/', userview, name='userview'),
    path('simulation/', simulation, name='simulation'),
    path('addproduct/', ProductFormView.as_view(), name='addproduct'),
    path('products/', ProductListView.as_view(), name='products'),
]
