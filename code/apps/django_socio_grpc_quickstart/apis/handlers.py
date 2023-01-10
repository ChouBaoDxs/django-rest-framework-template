from django_socio_grpc.utils.servicer_register import AppHandlerRegistry

from django_socio_grpc_quickstart.apis.services import QuestionService


def grpc_handlers(server):
    app_registry = AppHandlerRegistry('django_socio_grpc_quickstart', server)
    app_registry.register(QuestionService)
