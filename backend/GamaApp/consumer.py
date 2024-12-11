import json
import asyncio
import subprocess
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404

class SimulationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.simulation_id = self.scope['url_route']['kwargs']['simulation_id']
        self.simulation_group_name = f'simulation_{self.simulation_id}'

        # Join simulation group
        await self.channel_layer.group_add(
            self.simulation_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave simulation group
        await self.channel_layer.group_discard(
            self.simulation_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json['command']

        if command == 'run_simulation':
            await self.run_simulation()

    async def run_simulation(self):
        # Asegúrate de que las aplicaciones estén completamente cargadas
        await asyncio.sleep(1)

        from .models import Simulation
        simulation = await sync_to_async(get_object_or_404)(Simulation, id=self.simulation_id)

        # Aquí puedes ejecutar la simulación y enviar actualizaciones en tiempo real
        await self.run_gama_simulation()

    async def run_gama_simulation(self):
        # Ejecutar gama-headless.sh en un subproceso
        command = ["bash", "/path/to/gama-headless.sh", "-m", "4096m", "-socket"]

        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Leer la salida de la simulación en tiempo real
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            # Enviar cada línea de salida al WebSocket
            message = line.decode('utf-8').strip()
            await self.channel_layer.group_send(
                self.simulation_group_name,
                {
                    'type': 'simulation_update',
                    'message': message
                }
            )

        # Esperar a que termine el proceso
        await process.wait()

        # Cuando termine la simulación, enviar un mensaje de finalización
        await self.channel_layer.group_send(
            self.simulation_group_name,
            {
                'type': 'simulation_complete',
                'message': 'Simulation completed'
            }
        )

    async def simulation_update(self, event):
        message = event['message']
        # Enviar mensaje de actualización al WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def simulation_complete(self, event):
        message = event['message']
        # Enviar mensaje de finalización al WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
