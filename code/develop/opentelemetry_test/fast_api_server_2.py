import fastapi
from fastapi import Body
from pydantic import BaseModel
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from utils import init_jaeger_tracer

app = fastapi.FastAPI()


class UserInfo(BaseModel):
    name: str


tracer = trace.get_tracer(__name__)


@app.post('/server')
async def server(request: fastapi.Request, userinfo: str = Body(...), name: str = Body(..., )):
    return {'message': f'hello {userinfo},{name}'}


FastAPIInstrumentor.instrument_app(app, excluded_urls='/docs,/openapi.json')

if __name__ == '__main__':
    init_jaeger_tracer('fastapi-server-2')

    import uvicorn

    uvicorn.run(app, port=8001)
