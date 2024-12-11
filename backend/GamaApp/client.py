import asyncio
import json
import os
from asyncio import Future, TimeoutError
from typing import Dict, List
from gama_client.base_client import GamaBaseClient
from gama_client.command_types import CommandTypes
from gama_client.message_types import MessageTypes

SERVER_URL = "gama_headless"
SERVER_PORT = 6868
TIMEOUT = 120  # 2 minutos

class GamaClient(GamaBaseClient):
    async def start_listening_loop(self, handle_connection_message: bool):
        while True:
            try:
                mess = await self.socket.recv()
                try:
                    js = json.loads(mess)
                    if handle_connection_message and "type" in js and "content" in js and js["type"] == MessageTypes.ConnectionSuccessful.value:
                        self.connection_future.set_result(js["content"])
                    else:
                        await self.message_handler(js)
                except Exception as js_ex:
                    print("Unable to unpack gama-server messages as a json. Error:", js_ex, "Message received:", mess)
            except Exception as sock_ex:
                print("Error while waiting for a message from gama-server. Exiting", sock_ex)

async def run_simulation(id: str, experiment_name: str, gaml_file_path_on_server: str, init_parameters: List[Dict]):
    experiment_future: Future
    play_future: Future
    pause_future: Future
    expression_future: Future
    step_future: Future
    stop_future: Future

    async def _message_handler(message: Dict):
        print("received", message)
        if "command" in message:
            if message["command"]["type"] == CommandTypes.Load.value:
                experiment_future.set_result(message)
            elif message["command"]["type"] == CommandTypes.Play.value:
                play_future.set_result(message)
            elif message["command"]["type"] == CommandTypes.Pause.value:
                pause_future.set_result(message)
            elif message["command"]["type"] == CommandTypes.Expression.value:
                expression_future.set_result(message)
            elif message["command"]["type"] == CommandTypes.Step.value:
                step_future.set_result(message)
            elif message["command"]["type"] == CommandTypes.Stop.value:
                stop_future.set_result(message)

    # Validar init_parameters
    if not all(isinstance(param, dict) and "type" in param and "name" in param and "value" in param for param in init_parameters):
        raise ValueError("Los parámetros iniciales no están correctamente formateados.")

    client = GamaClient(SERVER_URL, SERVER_PORT, _message_handler)
    print("connecting to Gama server")
    await client.connect()

    print("initialize a gaml model")
    experiment_future = asyncio.get_running_loop().create_future()
    await client.load(gaml_file_path_on_server, experiment_name, True, True, True, True, init_parameters)
    gama_response = await experiment_future
    
    try:
        experiment_id = gama_response["content"]
    except Exception as e:
        print("error while initializing", gama_response, e)
        return

    print("initialization successful, running the model")
    results = []
    try:
        for _ in range(0, 60 * 24 * 55, 10):
            step_future = asyncio.get_running_loop().create_future()
            await asyncio.wait_for(client.step(experiment_id, 10, True), timeout=TIMEOUT)
            gama_response = await step_future
            if gama_response["type"] != MessageTypes.CommandExecutedSuccessfully.value:
                print("Unable to execute 10 new steps in the experiment", gama_response)
                break
            # Extraer datos reales de la respuesta de GAMA
            if "output" in gama_response:
                results.append(gama_response["output"])
    except TimeoutError:
        print(f"Simulation {id} timed out after {TIMEOUT} seconds")

    # Crear el directorio simulation_results si no existe
    results_dir = '/app/simulation_results'
    os.makedirs(results_dir, exist_ok=True)

    # Guardar los resultados en un archivo
    results_file = f'{results_dir}/results_{id}.json'
    print(f"Guardando resultados en: {results_file}")
    with open(results_file, 'w') as f:
        json.dump(results, f)
    
    return results_file