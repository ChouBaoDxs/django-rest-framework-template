import aiohttp
import fastapi
import requests
from fastapi import Body
from pydantic import BaseModel
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor

from utils import init_jaeger_tracer

app = fastapi.FastAPI()


class UserInfo(BaseModel):
    name: str


tracer = trace.get_tracer(__name__)


@app.post('/foobar')
async def foobar(userinfo: str = Body(...), name: str = Body(..., )):
    with tracer.start_as_current_span('foo'):
        with tracer.start_as_current_span('bar'):
            with tracer.start_as_current_span('baz'):
                print('Hello world from OpenTelemetry Python!')
    return {'message': f'hello {userinfo},{name}'}


@app.post('/foobar2')
async def foobar2(userinfo: str = Body(...), name: str = Body(..., )):
    return {'message': f'hello {userinfo},{name}'}


@app.post('/requests_client')
def requests_client(userinfo: str = Body(...), name: str = Body(..., )):
    json_data = {
        'userinfo': userinfo, 'name': name
    }
    res = requests.post('http://127.0.0.1:8001/server', json=json_data)
    return res.json()


@app.post('/aiohttp_client')
async def aiohttp_client(userinfo: str = Body(...), name: str = Body(..., )):
    json_data = {
        'userinfo': userinfo, 'name': name
    }
    async with aiohttp.ClientSession() as session:
        resp = await session.post('http://127.0.0.1:8001/server', json=json_data)
        return await resp.json()


@app.get('/django_server')
async def django_server():
    async with aiohttp.ClientSession() as session:
        resp = await session.get('http://127.0.0.1:8003/api/user/fake_success/')
        return await resp.json()


@app.get('/fake_error')
async def fake_error():
    x = 1
    y = 0
    a = x / y
    return a


RequestsInstrumentor().instrument()
AioHttpClientInstrumentor().instrument()
FastAPIInstrumentor.instrument_app(app, excluded_urls='/docs,/openapi.json')

if __name__ == '__main__':
    init_jaeger_tracer('fastapi-server-1')

    import uvicorn

    uvicorn.run(app, port=8000)
