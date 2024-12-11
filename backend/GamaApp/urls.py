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
    path('confirm_admin/<int:user_id>/<str:action>/', ConfirmAdminView.as_view(), name='confirm_admin'),
    path('confirm_delete_user/<int:user_id>/', ConfirmDeleteUserView.as_view(), name='confirm_delete_user'),
    path('assign_project/<int:user_id>/', AssignProjectView.as_view(), name='assign_project'),
    path('assign_simulation/<int:user_id>/<int:project_id>/', AssignSimulationView.as_view(), name='assign_simulation'),
    path('permissions/', PermissionsView.as_view(), name='permissions'),
    path('add_simulation/', ProjectListForSimulationView.as_view(), name='add_simulation'),
    path('select_simulation/<int:project_id>/', SelectSimulationView.as_view(), name='select_simulation'),
    path('process_simulation/<int:project_id>/', ProcessSimulationView.as_view(), name='process_simulation'),
    path('select_parameters/<int:simulation_id>/', SelectParameterView.as_view(), name='select_parameters'),
    path('edit_running_parameters/<int:simulation_id>/', EditRunningParametersView.as_view(), name='edit_running_parameters'),
    path('delete_simulation/', DeleteSimulationView.as_view(), name='delete_simulation'),
    path('add_project/', AddProjectView.as_view(), name='add_project'),
    path('edit_project/', ProjectListView.as_view(), name='edit_project'),

    path('edit_simulation_parameters/<int:user_id>/<int:simulation_id>/', EditSimulationParametersView.as_view(), name='edit_simulation_parameters'),
    path('edit_project/<int:pk>/', EditProjectView.as_view(), name='edit_project_detail'),
    path('delete_project/', ProjectListView.as_view(), name='delete_project'),
    path('confirm_delete_project/<int:pk>/', DeleteProjectView.as_view(), name='confirm_delete_project'),
    path('project_simulation_list/', ProjectSimulationListView.as_view(), name='project_simulation_list'),
    path('edit_simulation/<int:simulation_id>/', EditSimulationView.as_view(), name='edit_simulation'),
    path('simulation_results/<int:simulation_id>/', ViewSimulationResultsView.as_view(), name='view_simulation_results'),
    path('run_simulation/<int:simulation_id>/', RunSimulationView.as_view(), name='run_simulation'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)