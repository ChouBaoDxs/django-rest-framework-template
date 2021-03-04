from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

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

app_name = "apis"
urlpatterns = defalt_router.urls + [
    path(r"user/", include(user_router.urls)),
]
