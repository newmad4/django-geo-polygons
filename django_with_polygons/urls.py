from typing import Optional

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.request import Request


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(
        self, request: Optional[Request] = None, public: bool = False
    ) -> openapi.Swagger:
        schema = super().get_schema(request, public)
        schema.schemes = ["https"]
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title="Mozio API Schema",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=BothHttpAndHttpsSchemaGenerator,
)

urlpatterns = [
    path("api/v1/", include("provider.urls")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
