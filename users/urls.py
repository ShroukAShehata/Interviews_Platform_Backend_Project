
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)
from users.views import RegisterView , LogoutView, LoginView


urlpatterns = [
    
   #__ Authentication __#
    #Sign Up
    path("api/auth/signup/", RegisterView.as_view(), name="register"),
    # POST {username,password} => {access, refresh}
    path("api/auth/login/", LoginView.as_view(), name="token_obtain_pair"),
    # POST {refresh} => {access}
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Verify token
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # Logout
    path("api/auth/logout/", LogoutView.as_view(), name="auth_logout"),
]

