from sys import argv

import requests

from opentelemetry import trace
from opentelemetry.propagate import inject

from utils import init_console_tracer


def direct():
    with tracer.start_as_current_span('client'):
        with tracer.start_as_current_span('client-server'):
            headers = {}
            inject(headers)
            res = requests.get(
                'http://0.0.0.0:8003/api/user/fake_success/',
                # params={'param': argv[1]},
                params={'param': 'hello'},
                headers=headers,
            )

            assert res.status_code == 200


def requests_instrumentor():
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    RequestsInstrumentor().instrument()  # 不再需要手动设置 inject(headers)
    with tracer.start_as_current_span('client'):
        with tracer.start_as_current_span('client-server'):
            res = requests.get(
                'http://0.0.0.0:8003/api/user/fake_success/',
                # params={'param': argv[1]},
                params={'param': 'hello'},
            )
            assert res.status_code == 200


if __name__ == '__main__':
    init_console_tracer('requests-client')
    tracer = trace.get_tracer_provider().get_tracer(__name__)

    direct()
    requests_instrumentor()
