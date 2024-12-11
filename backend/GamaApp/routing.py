from django.urls import re_path
from . import consumer

websocket_urlpatterns = [
    re_path(r'ws/simulation/(?P<simulation_id>\d+)/$', consumer.SimulationConsumer.as_asgi()),
]