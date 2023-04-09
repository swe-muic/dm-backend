"""dm_backend URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from .src.views.equation import EquationAPIViewSet
from .src.views.equation_parser import EquationParserAPI
from .src.views.graph import GraphAPI

router = routers.DefaultRouter()
router.register(r"api/viewset/equations", EquationAPIViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("api/equations/parser/", EquationParserAPI.as_view(http_method_names=["get"])),
    path("api/graphs/", GraphAPI.as_view(http_method_names=["get", "post"])),
    path(
        "api/graphs/<int:graph_id>/",
        GraphAPI.as_view(http_method_names=["get", "put", "delete"]),
    ),
]
