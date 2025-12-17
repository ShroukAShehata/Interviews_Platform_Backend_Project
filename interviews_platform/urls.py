
from django.urls import path, include
from django.contrib import admin

from drf_spectacular.views import (SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView,)


urlpatterns = [

    path('admin/', admin.site.urls),

    #__ Documentation __#
    # OpenAPI Schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Swagger UI
    path("api/docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    # Redoc UI
    path("api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc-ui"),

    path('api/v1/auth/', include('users.urls')),
    path('api/v1/', include('questions.urls')),
]
