from django.contrib import admin
from django.urls import path, include
from account.urls import urlpatterns as auth
from techno.urls import urlpatterns as techno
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title='DRFTechno API',
        default_version='v1',
        description='Document for techno'
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include(auth)),
    path('api/v1/', include(techno)),
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/v1/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
