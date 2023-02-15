import aiohttp
import fastapi
import requests
from fastapi import Body
from pydantic import BaseModel
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
from opentelemetry.sdk.trace import TracerProvider, Span

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


def server_request_hook(span: Span, scope: dict):
    if span and span.is_recording():
        span.set_attribute('custom_user_attribute_from_request_hook', 'some-value')


def client_request_hook(span: Span, scope: dict):
    if span and span.is_recording():
        span.set_attribute('custom_user_attribute_from_client_request_hook', 'some-value')


def client_response_hook(span: Span, message: dict):
    if span and span.is_recording():
        span.set_attribute('custom_user_attribute_from_response_hook', 'some-value')


@app.middleware('http')
async def add_trace_id_header(request: fastapi.Request, call_next):
    response = await call_next(request)
    # trace_id = trace.get_current_span().get_span_context().trace_id
    span: Span = trace.get_current_span()
    if span.is_recording():
        trace_id = span.context.trace_id
        # trace_id = span.get_span_context().trace_id
        response.headers['trace-id'] = trace.format_trace_id(trace_id)
    return response


RequestsInstrumentor().instrument()
AioHttpClientInstrumentor().instrument()
FastAPIInstrumentor.instrument_app(
    app,
    excluded_urls='/docs,/openapi.json',
    server_request_hook=server_request_hook,
    client_request_hook=client_request_hook,
    client_response_hook=client_response_hook,
)

if __name__ == '__main__':
    init_jaeger_tracer('fastapi-server-1')

    import uvicorn

    uvicorn.run(app, port=8000)
