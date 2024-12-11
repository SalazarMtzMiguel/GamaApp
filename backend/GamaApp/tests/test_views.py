from django.test import TestCase
from django.urls import reverse
from .test_models import Simulation, Project, Parameter

class RunSimulationViewTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name="Test Project")
        self.simulation = Simulation.objects.create(
            project=self.project,
            file="test.gaml",
            experiment_name="Test Experiment"
        )
        self.parameter = Parameter.objects.create(
            data_type="int",
            variable_name="test_param",
            value="10",
            active=True
        )
        self.simulation.parameters.add(self.parameter)

    def test_run_simulation_view(self):
        response = self.client.post(reverse('run_simulation', args=[self.simulation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Simulación en ejecución')

    def test_view_simulation_results_view(self):
        response = self.client.get(reverse('view_simulation_results', args=[self.simulation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Resultados no encontrados')

class ViewSimulationResultsViewTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name="Test Project")
        self.simulation = Simulation.objects.create(
            project=self.project,
            file="test.gaml",
            experiment_name="Test Experiment"
        )

    def test_view_simulation_results_view(self):
        response = self.client.get(reverse('view_simulation_results', args=[self.simulation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Resultados no encontrados')

class RunSimulationViewTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name="Test Project")
        self.simulation = Simulation.objects.create(
            project=self.project,
            file="test.gaml",
            experiment_name="Test Experiment"
        )
        self.parameter = Parameter.objects.create(
            data_type="int",
            variable_name="test_param",
            value="10",
            active=True
        )
        self.simulation.parameters.add(self.parameter)

    def test_run_simulation_view(self):
        response = self.client.post(reverse('run_simulation', args=[self.simulation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Simulación en ejecución')

    def test_run_simulation_view_no_parameters(self):
        self.simulation.parameters.clear()
        response = self.client.post(reverse('run_simulation', args=[self.simulation.id]))
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'No hay parámetros válidos activos para esta simulación')

    def test_view_simulation_results_view(self):
        response = self.client.get(reverse('view_simulation_results', args=[self.simulation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Resultados no encontrados')

class ViewSimulationResultsViewTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name="Test Project")
        self.simulation = Simulation.objects.create(
            project=self.project,
            file="test.gaml",
            experiment_name="Test Experiment"
        )

    def test_view_simulation_results_view(self):
        response = self.client.get(reverse('view_simulation_results', args=[self.simulation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Resultados no encontrados')


class RunSimulationViewTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name="Test Project")
        self.simulation = Simulation.objects.create(
            project=self.project,
            file="test.gaml",
            experiment_name="Test Experiment"
        )
        self.parameter = Parameter.objects.create(
            data_type="int",
            variable_name="test_param",
            value="10",
            active=True
        )
        self.simulation.parameters.add(self.parameter)

    def test_run_simulation_view(self):
        response = self.client.post(reverse('run_simulation', args=[self.simulation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Simulación en ejecución')

    def test_run_simulation_view_no_parameters(self):
        self.simulation.parameters.clear()
        response = self.client.post(reverse('run_simulation', args=[self.simulation.id]))
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'No hay parámetros válidos activos para esta simulación')

    def test_view_simulation_results_view(self):
        response = self.client.get(reverse('view_simulation_results', args=[self.simulation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Resultados no encontrados')

class ViewSimulationResultsViewTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name="Test Project")
        self.simulation = Simulation.objects.create(
            project=self.project,
            file="test.gaml",
            experiment_name="Test Experiment"
        )

    def test_view_simulation_results_view(self):
        response = self.client.get(reverse('view_simulation_results', args=[self.simulation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Resultados no encontrados')