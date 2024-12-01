from rest_framework.routers import DefaultRouter

from django.urls import path, include

from . import views


app_name = 'income'

router = DefaultRouter()
router.register('income', views.IncomeViewSet, basename='income')
router.register('expenses', views.ExpenseViewSet, basename='expense')
urlpatterns = [
    path('', include(router.urls)),
]
