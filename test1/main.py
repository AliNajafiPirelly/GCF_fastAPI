from multiprocessing import Process
import os
from flask import Request
from fastapi import FastAPI
from localpackage.api_manager import APIManager
from localpackage.gateway_manager import GatewayManager
from localpackage.types import APIConfig,GatewayConfig

API_STARTED_NAME = 'API_STARTED'
os.environ[API_STARTED_NAME] = '0'

api = APIManager(APIConfig(name='testAPI'),FastAPI())
app = api.as_app()

adaptor = GatewayManager(
    config=GatewayConfig(is_debug=True),
    api_manager=api
)

@app.get('/ping')
def get_hello():
    """some example function"""
    return "pong"


def mock_func(req:Request):
    return adaptor.manage(req)
