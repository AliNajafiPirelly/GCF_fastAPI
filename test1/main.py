from multiprocessing import Process
import os
from flask import Request
from fastapi import FastAPI
import uvicorn


app = FastAPI()
start = False
fapi_prcss = None 

@app.get('/')
def get_hello():
    """some example function"""
    return {'hello':'world'}

def start_fastapi():
    print('fast api starting ...')
    global start
    if not start:
        trd = Process(target=uvicorn.run,kwargs={"app":"main:app","port":5060,"host":"localhost"})
        start = True
        return trd

def stop_fastapi(prcss:Process):
    print('stopping the server')
    prcss.terminate()

        

def mock_func(req:Request):
    print(os.getpid())
    global start
    global fapi_prcss
    if not start:
        if req.headers.get('X-Start-Api','') == '1':
            if req.authorization:
                if req.authorization.token == 'authorize':
                    fapi_prcss = start_fastapi()
                    fapi_prcss.start()
                    start = True
                    return f"fast api running on Process {fapi_prcss.pid}",200
    
    if req.headers.get('X-STOP-API','') == '1':
        if req.authorization:
            if req.authorization.token == 'authorize':
                if start:
                    if fapi_prcss:
                        stop_fastapi(fapi_prcss)
                        start = False
                        return f"fast api stopped"
    
    return {
        "args":req.args,
        "scheme":req.scheme,
        "authorization":getattr(req,'authorization',None),
        "base_url":req.base_url,
        "blueprints":req.blueprints,
        "content_length":req.content_length,
        "headers":{k:req.headers.get(k) for k in req.headers.keys()},
        "endpoint":req.endpoint,
        "is_json":req.is_json,
        "data":req.data.decode('utf-8'),
        "cookies":list(req.cookies.lists()),
        "environ":list(req.environ.keys()),
        'method' : req.method,
        'query' : req.query_string.decode('utf-8')
    },200



