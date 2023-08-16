from rest_framework_extensions.routers import ExtendedSimpleRouter

from generate_crud_code_example.apis.views.book import BookViewSet

router = ExtendedSimpleRouter()

router.register('book', BookViewSet, basename='book')

urlpatterns = router.urls
