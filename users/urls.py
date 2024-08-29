from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.authtoken.views import obtain_auth_token

from users.views import UserViewSet

router = SimpleRouter()

router.register(r'users', UserViewSet)

urlpatterns = [
    path('token/', obtain_auth_token)
]

urlpatterns += router.urls
