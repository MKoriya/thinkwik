from django.contrib import admin
from django.urls import path, include
from school.jwt import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/', include("user.urls")),
    path('api/v1/auth/token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
