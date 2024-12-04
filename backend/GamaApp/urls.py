from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from GamaApp.views import *

urlpatterns = [
    path('', my_view, name='index'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('userview/', userview, name='userview'),
    path('simulations/', SimulationsView.as_view(), name='simulations'),
    path('about/', about, name='about'),
    path('faq/', faq, name='faq'),
    path('adminview/', AdminView.as_view(), name='adminview'),
    path('permissions/', PermissionsView.as_view(), name='permissions'),
    path('add_simulation/', ProjectListForSimulationView.as_view(), name='add_simulation'),
    path('select_simulation/<int:project_id>/', SelectSimulationView.as_view(), name='select_simulation'),
    path('process_simulation/<int:project_id>/', ProcessSimulationView.as_view(), name='process_simulation'),
    path('select_parameters/<int:simulation_id>/', SelectParameterView.as_view(), name='select_parameters'),
    path('run_simulation/<int:simulation_id>/', run_simulation, name='run_simulation'),
    path('edit_simulation/', EditSimulationView.as_view(), name='edit_simulation'),
    path('delete_simulation/', DeleteSimulationView.as_view(), name='delete_simulation'),
    path('add_project/', AddProjectView.as_view(), name='add_project'),
    path('edit_project/', ProjectListView.as_view(), name='edit_project'),
    path('edit_project/<int:pk>/', EditProjectView.as_view(), name='edit_project_detail'),
    path('delete_project/', ProjectListView.as_view(), name='delete_project'),
    path('confirm_delete_project/<int:pk>/', DeleteProjectView.as_view(), name='confirm_delete_project'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)