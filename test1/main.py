from multiprocessing import Process
import os
from flask import Request
from fastapi import FastAPI
from localpackage.api_manager import APIManager
from localpackage.types import APIConfig

API_STARTED_NAME = 'API_STARTED'
os.environ[API_STARTED_NAME] = '0'

api = APIManager(APIConfig(name='testAPI'),FastAPI())
app = api.as_app()

@app.get('/ping')
def get_hello():
    """some example function"""
    return "pong"

def mock_func(req:Request):

    if os.environ.get(API_STARTED_NAME) == '0':
        api.start()
        os.environ[API_STARTED_NAME] = '1'
    
    return {
        "args":req.args,
        "scheme":req.scheme,
        "authorization":getattr(req,'authorization',None),
        "base_url":req.base_url,
        "blueprints":req.blueprints,
        "content_length":req.content_length,
        "headers":{k:v for k,v in req.headers.items()},
        "endpoint":req.endpoint,
        "is_json":req.is_json,
        "data":req.data.decode('utf-8'),
        "cookies":list(req.cookies.lists()),
        "environ":list(req.environ.keys()),
        'method' : req.method,
        'query' : req.query_string.decode('utf-8'),
        'path' : req.path,
    },200
