import asyncio
import os
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from client import run_simulation

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/run_simulation/")
async def run_experiment(id: str, name: str, path: str):
    results_file = await run_simulation(id=id, experiment_name=name, gaml_file_path_on_server=path)
    return {"results_file": results_file}

@app.get("/results/{file_name}")
def get_results(file_name: str):
    path = f"/app/simulation_results/{file_name}"
    if os.path.isfile(path):
        return FileResponse(path)
    return Response(status_code=404)