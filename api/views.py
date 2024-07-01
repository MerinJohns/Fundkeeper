from django.shortcuts import render

from django.utils import timezone

from django.db.models import Sum

from rest_framework.response import Response

from rest_framework.views import APIView

from api.serializers import UserSerializer,ExpenseSerializer,IncomeSerializer

from rest_framework.viewsets import ModelViewSet

from budget.models import Expense,Income

from rest_framework import authentication,permissions

from api.permissions import OwnerOnly


class UserCreationView(APIView):

    def post(self,request,*args,**kwargs):

        serializer_instance=UserSerializer(data=request.data) #deserialize

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)


class ExpenseViewSet(ModelViewSet):

    serializer_class=ExpenseSerializer

    queryset=Expense.objects.all()

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[OwnerOnly]

    def list(self,request,*args,**kwargs):

        qs=Expense.objects.filter(user_object=request.user)

        serializer_instance=ExpenseSerializer(qs,many=True)

        return Response(data=serializer_instance.data)

    def perform_create(self, serializer):

        return serializer.save(user_object=self.request.user)


class IncomeViewSet(ModelViewSet):

    serializer_class=IncomeSerializer

    queryset=Income.objects.all()

    authentication_classes=[authentication.TokenAuthentication]

    #permission_classes=[permissions.IsAuthenticated]

    permission_classes=[OwnerOnly]


    def list(self,request,*args,**kwargs):

        qs=Income.objects.filter(user_object=request.user)

        serializer_instance=IncomeSerializer(qs,many=True)

        return Response(data=serializer_instance.data)

    def perform_create(self, serializer):

        return serializer.save(user_object=self.request.user)


class ExpenseSummary(APIView):

    permission_classes=[permissions.IsAuthenticated]

    authentication_classes=[authentication.TokenAuthentication]

    def get(self,request,*args,**kwargs):

        current_month=timezone.now().month

        current_year=timezone.now().year

        all_expenses=Expense.objects.filter(

            user_object=request.user,

            created_date__month=current_month,

            created_date__year=current_year
        )

        expense_total=all_expenses.values("amount").aggregate(total=Sum("amount"))

        #print(expense_total)

        category_summary=all_expenses.values("category").annotate(total=Sum("amount"))

        priority_summary=all_expenses.values("priority").annotate(total=Sum("amount"))

        data={

            "total_expense":expense_total,

            "category_summary":category_summary,

            "priority_summary":priority_summary
        }

        return Response(data=data)



class IncomeSummary(APIView):

    permission_classes=[permissions.IsAuthenticated]

    authentication_classes=[authentication.TokenAuthentication]

    def get(self,request,*args,**kwargs):

        current_month=timezone.now().month

        current_year=timezone.now().year

        all_incomes=Income.objects.filter(

            user_object=request.user, 

            created_date__month=current_month,

            created_date__year=current_year
        )

        income_total=all_incomes.values("amount").aggregate(total=Sum("amount"))

        #print(income_total)

        category_summary=all_incomes.values("category").annotate(total=Sum("amount"))

        data={

            "total_income":income_total,

            "category_summary":category_summary,
        }

        return Response(data=data)