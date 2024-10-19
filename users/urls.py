from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from materials.views import PaymentCreateAPIView
from users.apps import UsersConfig
from users.views import UserCreateAPIView, SubscriptionAPIView
from users.views import UserViewSet, PaymentsViewSet

app_name = UsersConfig.name
router = SimpleRouter()

router.register('', UserViewSet)
router.register('payments', PaymentsViewSet)

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path('subscription/', SubscriptionAPIView.as_view(), name='subscription-api'),
    path('payment/', PaymentCreateAPIView.as_view(), name='payment'),
]

urlpatterns += router.urls
