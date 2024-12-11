from django.test import TestCase
from .test_models import Simulation, Project, Parameter

class ProjectModelTest(TestCase):
    def test_project_creation(self):
        project = Project.objects.create(name="Test Project")
        self.assertEqual(project.name, "Test Project")

class SimulationModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name="Test Project")

    def test_simulation_creation(self):
        simulation = Simulation.objects.create(
            project=self.project,
            file="test.gaml",
            experiment_name="Test Experiment"
        )
        self.assertEqual(simulation.project.name, "Test Project")
        self.assertEqual(simulation.file, "test.gaml")
        self.assertEqual(simulation.experiment_name, "Test Experiment")

class ParameterModelTest(TestCase):
    def test_parameter_creation(self):
        parameter = Parameter.objects.create(
            data_type="int",
            variable_name="test_param",
            value="10",
            active=True
        )
        self.assertEqual(parameter.data_type, "int")
        self.assertEqual(parameter.variable_name, "test_param")
        self.assertEqual(parameter.value, "10")
        self.assertTrue(parameter.active)

from django.test import TestCase
from .models import Simulation, Project, Parameter

class ProjectModelTest(TestCase):
    def test_project_creation(self):
        project = Project.objects.create(name="Test Project")
        self.assertEqual(project.name, "Test Project")

class SimulationModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name="Test Project")

    def test_simulation_creation(self):
        simulation = Simulation.objects.create(
            project=self.project,
            file="test.gaml",
            experiment_name="Test Experiment"
        )
        self.assertEqual(simulation.project.name, "Test Project")
        self.assertEqual(simulation.file, "test.gaml")
        self.assertEqual(simulation.experiment_name, "Test Experiment")

    def test_simulation_parameters(self):
        simulation = Simulation.objects.create(
            project=self.project,
            file="test.gaml",
            experiment_name="Test Experiment"
        )
        parameter = Parameter.objects.create(
            data_type="int",
            variable_name="test_param",
            value="10",
            active=True
        )
        simulation.parameters.add(parameter)
        self.assertIn(parameter, simulation.parameters.all())

class ParameterModelTest(TestCase):
    def test_parameter_creation(self):
        parameter = Parameter.objects.create(
            data_type="int",
            variable_name="test_param",
            value="10",
            active=True
        )
        self.assertEqual(parameter.data_type, "int")
        self.assertEqual(parameter.variable_name, "test_param")
        self.assertEqual(parameter.value, "10")
        self.assertTrue(parameter.active)