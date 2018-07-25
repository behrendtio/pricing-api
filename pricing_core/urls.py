# pricing_core/urls.py

from django.conf.urls import url, include

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'orders', views.OrderViewSet, "orders")


urlpatterns = [
    url(r'^', include(router.urls)),
    # API authntication can be a further development
]
