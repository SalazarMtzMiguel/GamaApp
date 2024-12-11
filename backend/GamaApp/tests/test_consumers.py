from channels.testing import WebsocketCommunicator
from django.test import TestCase
from .test_consumers import SimulationConsumer
from .test_models import Simulation, Project

class SimulationConsumerTest(TestCase):
    async def test_run_simulation(self):
        project = Project.objects.create(name="Test Project")
        simulation = Simulation.objects.create(
            project=project,
            file="test.gaml",
            experiment_name="Test Experiment"
        )

        communicator = WebsocketCommunicator(SimulationConsumer, f"/ws/simulation/{simulation.id}/")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

        await communicator.send_json_to({
            'command': 'run_simulation'
        })

        response = await communicator.receive_json_from()
        self.assertEqual(response['message'], 'Simulation completed')

        await communicator.disconnect()

class SimulationConsumerTest(TestCase):
    async def test_run_simulation(self):
        project = Project.objects.create(name="Test Project")
        simulation = Simulation.objects.create(
            project=project,
            file="test.gaml",
            experiment_name="Test Experiment"
        )

        communicator = WebsocketCommunicator(SimulationConsumer, f"/ws/simulation/{simulation.id}/")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

        await communicator.send_json_to({
            'command': 'run_simulation'
        })

        response = await communicator.receive_json_from()
        self.assertEqual(response['message'], 'Simulation completed')

        await communicator.disconnect()

from channels.testing import WebsocketCommunicator
from django.test import TestCase
from .consumers import SimulationConsumer
from .models import Simulation, Project

class SimulationConsumerTest(TestCase):
    async def test_run_simulation(self):
        project = Project.objects.create(name="Test Project")
        simulation = Simulation.objects.create(
            project=project,
            file="test.gaml",
            experiment_name="Test Experiment"
        )

        communicator = WebsocketCommunicator(SimulationConsumer, f"/ws/simulation/{simulation.id}/")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

        await communicator.send_json_to({
            'command': 'run_simulation'
        })

        response = await communicator.receive_json_from()
        self.assertEqual(response['message'], 'Simulation completed')

        await communicator.disconnect()

    async def test_invalid_command(self):
        project = Project.objects.create(name="Test Project")
        simulation = Simulation.objects.create(
            project=project,
            file="test.gaml",
            experiment_name="Test Experiment"
        )

        communicator = WebsocketCommunicator(SimulationConsumer, f"/ws/simulation/{simulation.id}/")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

        await communicator.send_json_to({
            'command': 'invalid_command'
        })

        response = await communicator.receive_json_from()
        self.assertEqual(response['message'], 'Invalid command')

        await communicator.disconnect()

