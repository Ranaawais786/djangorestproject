"""userapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include


from Home.api.V1 import viewsets
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('daily-quote', viewsets.DailyQuoteview, basename='quote'),
router.register('smile', viewsets.Smileview, basename='smile'),
# router.register('bestday', viewsets.BestDayViewSet, basename='bestday'),
router.register('user_goal', viewsets.GoalView, basename='UserGoal'),
router.register('activity', viewsets.AcitivityViewset, basename='activity'),
router.register('favourite', viewsets.FavouriteViewset, basename="fav"),
router.register('community', viewsets.CommnityViewset, basename='community'),
router.register('resource', viewsets.resourceViewSet, basename='resource'),
router.register('smile_science', viewsets.SmilescienceViewset, basename="smile_science"),
urlpatterns = [
    path('',include(router.urls)),

    path('register/', viewsets.CreateUserViewMy.as_view()),
    # path('auth', include('rest_framework.urls', namespace='rest_framework')),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('login/', viewsets.Login.as_view()),

]
