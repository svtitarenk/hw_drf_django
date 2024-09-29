from django.urls import path
from rest_framework.routers import SimpleRouter
from users.apps import UsersConfig
from users.views import UserViewSet, PaymentsViewSet

app_name = UsersConfig.name
router = SimpleRouter()

router.register('', UserViewSet)
router.register('payments', PaymentsViewSet)

# urlpatterns = []

urlpatterns = router.urls
