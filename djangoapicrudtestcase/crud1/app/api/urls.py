from django.template.defaulttags import url
from django.urls import include, path

from .viewset import InformationViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('crud', InformationViewSet, basename='test')
urlpatterns = [
    path('first/', include((router.urls, 'app'), namespace='first')),

]
