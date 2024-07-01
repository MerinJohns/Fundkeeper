from django.urls import path

from api import views

from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework.routers import DefaultRouter

router=DefaultRouter()

router.register("expenses",views.ExpenseViewSet, basename="expenses")

router.register("incomes",views.IncomeViewSet, basename="incomes")

urlpatterns=[

    path("register/",views.UserCreationView.as_view()),

    path("income/summary/",views.IncomeSummary.as_view()),

    path("expense/summary/",views.ExpenseSummary.as_view()),

    path("token/",ObtainAuthToken.as_view()),

]+router.urls