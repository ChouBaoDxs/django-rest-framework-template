from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from test_demo.views import ProductViewSet
from user.apis.views import (
    UserViewSet,
    UserProfileViewSet,
)

if settings.DEBUG:
    Router = DefaultRouter
else:
    Router = SimpleRouter

# base
defalt_router = Router()

# user app
user_router = Router()
user_router.register('', UserViewSet, basename='user')
user_router.register('user_profile', UserProfileViewSet, basename='user_profile')

# test_demo app
test_demo_router = Router()
test_demo_router.register('product', ProductViewSet, basename='product')

app_name = "apis"
urlpatterns: list = defalt_router.urls + [
    path(r'user/', include(user_router.urls)),
    path(r'test-demo/', include(test_demo_router.urls)),
]

if settings.DEBUG:
    def trigger_error(request):
        division_by_zero = 1 / 0


    urlpatterns.append(path('sentry-debug/', trigger_error))
