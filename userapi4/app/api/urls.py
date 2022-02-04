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

from app.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('employee', views.EmployeeView, basename='employee'),
router.register('category', views.CategoryView, basename='catagory'),
router.register('bookingRequest', views.BookingView, basename='booking'),
router.register('UserbookingRequest', views.UserBookingView, basename='Userbooking'),
router.register('UserRating', views.RatingView, basename='rating'),
router.register('employeecategory', views.EmployeeCtView, basename='ebooking'),
urlpatterns = [
    path('',include(router.urls)),
    path('register/', views.CreateUserViewMy.as_view()),
    path('auth', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', views.Login.as_view()),

]
