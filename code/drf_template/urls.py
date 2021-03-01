"""drf_template URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
import xadmin

urlpatterns = [
    # path('admin/', admin.site.urls),
    path(f'{settings.XADMIN_URL}/', xadmin.site.urls),
    path("api/", include("drf_template.api_router")),
]

if settings.DEBUG or settings.OPEN_SWAGGER:
    # 下面这种两写法在DEBUG=False时不会处理静态文件
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    # urlpatterns += staticfiles_urlpatterns()

    # swagger 文档部分
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi
    from rest_framework import permissions
    from rest_framework.documentation import include_docs_urls

    schema_view = get_schema_view(
        openapi.Info(
            title="Swagger Doc",
            default_version='v1',
            description="description",
            # terms_of_service="https://www.google.com/policies/terms/",
            # contact=openapi.Contact(email="contact@snippets.local"),
            # license=openapi.License(name="BSD License"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    urlpatterns += [
        url(r'^xadmin/', xadmin.site.urls),
        # 原生core文档
        url(r'^docs/', include_docs_urls(title="Doc", authentication_classes=[], permission_classes=[])),
        # swagger文档
        url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]

if not settings.DEBUG:
    # DEBUG=False时处理静态文件
    urlpatterns += [url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}, name='static')]
