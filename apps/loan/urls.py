from django.urls import path, include

from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('', views.LoanViwSet, basename='loan')


app_name = 'loan'
urlpatterns = [
    path('', include(router.urls))
]

