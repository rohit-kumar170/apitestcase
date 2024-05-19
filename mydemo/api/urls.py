from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('product/', ProductViewSet.as_view({"get":"list","post":"create"}), name='product'),
    path('product/<int:id>/', ProductViewSet.as_view({"get":"retrieve","patch":"partial_update","delete":"destroy"}), name='product'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
