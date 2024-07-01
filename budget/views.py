from django.shortcuts import render,redirect
from django.views.generic import View
from budget.forms import ExpenseForm,RegistrationForm,LoginForm,SummaryForm
from budget.forms import IncomeForm
from budget.models import Expense
from budget.models import Income
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login,logout
from budget.decorators import signin_required
from django.utils.decorators import method_decorator
import datetime

# Create your views here.
@method_decorator(signin_required,name="dispatch")
class ExpenseCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=ExpenseForm()

        # qs=Expense.objects.all()

        qs=Expense.objects.filter(user_object=request.user).order_by("-created_date")

        return render(request,"expense_add.html",{"form":form_instance,"data":qs})

    def post(self,request,*args,**kwargs):

        form_instance=ExpenseForm(request.POST)

        if form_instance.is_valid():

            #we have to add user_object to form_instance before saving form_instance

            form_instance.instance.user_object=request.user #adding user_object

            form_instance.save() #missing user_object

            messages.success(request,"expense created!!!")

            print("expense has been created")

            return redirect("expense-add")

        else:

            messages.error(request,"failed to create!!!")

            return render(request,"expense_add.html",{"form":form_instance})


@method_decorator(signin_required,name="dispatch")
class ExpenseUpdateView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        expense_object=Expense.objects.get(id=id)

        form_instance=ExpenseForm(instance=expense_object)

        return render(request,"expense_edit.html",{"form":form_instance})

    
    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        expense_object=Expense.objects.get(id=id)

        form_instance=ExpenseForm(instance=expense_object,data=request.POST)

        if form_instance.is_valid():

            form_instance.save()

            messages.success(request,"expense updated!!!")

            return redirect("expense-add")

        else:

            messages.error(request,"failed to update!!!")

            return render(request,"expense_edit.html",{"form":form_instance})

@method_decorator(signin_required,name="dispatch")
class ExpenseDetailView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Expense.objects.get(id=id)

        return render(request,"expense_detail.html",{"data":qs})

@method_decorator(signin_required,name="dispatch")
class ExpenseDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Expense.objects.get(id=id).delete()

        messages.success(request,"expense deleted!!!")

        return redirect("expense-add")


@method_decorator(signin_required,name="dispatch")
class IncomeCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=IncomeForm()

        #qs=Income.objects.all()

        qs=Income.objects.filter(user_object=request.user).order_by("-created_date")

        return render(request,"income_add.html",{"form":form_instance,"data":qs})

    def post(self,request,*args,**kwargs):

        form_instance=IncomeForm(request.POST)

        if form_instance.is_valid():

            form_instance.instance.user_object=request.user

            form_instance.save()

            messages.success(request,"income created")

            print("income has been created")

            return redirect("income-add")

        else:

            messages.error(request,"failed to create!!")

            return render(request,"income_add.html",{"form":form_instance})

@method_decorator(signin_required,name="dispatch")
class IncomeUpdateView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        income_object=Income.objects.get(id=id)

        form_instance=IncomeForm(instance=income_object)

        return render(request,"income_edit.html",{"form":form_instance})

    
    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        income_object=Income.objects.get(id=id)

        form_instance=IncomeForm(instance=income_object,data=request.POST)

        if form_instance.is_valid():

            form_instance.save()

            messages.success(request,"income updated!!!")

            return redirect("income-add")

        else:

            messages.error(request,"failed to update!!!")

            return render(request,"income_edit.html",{"form":form_instance})

@method_decorator(signin_required,name="dispatch")
class IncomeDetailView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Income.objects.get(id=id)

        return render(request,"income_detail.html",{"data":qs})

@method_decorator(signin_required,name="dispatch")
class IncomeDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Income.objects.get(id=id).delete()

        messages.success(request,"income deleted!!!")

        return redirect("income-add")

@method_decorator(signin_required,name="dispatch")
class ExpenseSummaryView(View):

    def get(self,request,*args,**kwargs):

        current_month=timezone.now().month

        current_year=timezone.now().year

        expense_list=Expense.objects.filter(created_date__month=current_month,created_date__year=current_year,user_object=request.user)

        expense_total=expense_list.values("amount").aggregate(total=Sum("amount"))

        print(expense_total)

        category_sum=expense_list.values("category").annotate(total=Sum("amount"))

        print(category_sum)

        priority_sum=expense_list.values("priority").annotate(total=Sum("amount"))

        print(priority_sum)

        data={
            "expense_total":expense_total,
            "category_sum":category_sum,
            "priority_sum":priority_sum
        }

        return render(request,"expense_summary.html",data)

@method_decorator(signin_required,name="dispatch")
class IncomeSummaryView(View):

    def get(self,request,*args,**kwargs):

        current_month=timezone.now().month

        current_year=timezone.now().year

        income_list=Income.objects.filter(created_date__month=current_month,created_date__year=current_year,user_object=request.user)

        income_total=income_list.values("amount").aggregate(total=Sum("amount"))

        print(income_total)

        category_sum=income_list.values("category").annotate(total=Sum("amount"))

        print(category_sum)

        data={
            "income_total":income_total,
            "category_sum":category_sum
        }

        return render(request,"income_summary.html",data)


class SignUpView(View):

    def get(self,request,*args,**kwargs):

        form_instance=RegistrationForm()

        return render(request,"register.html",{"form":form_instance})


    def post(self,request,*args,**kwargs):


        form_instance=RegistrationForm(request.POST)

        if form_instance.is_valid():

            # form_instance.save() # here creating a user object, here password willnot encrypted #user.objects.create() work chythale password encrypt aakullu

            data=form_instance.cleaned_data

            User.objects.create_user(**data)#this will encrypt the password

            print("user created")

            return redirect("signin")

        else:

            print("user creation failed")

            return render(request,"register.html",{"form":form_instance})

#login


class SignInView(View):

    def get(self,request,*args,**kwargs):

        form_instance=LoginForm()

        return render(request,"login.html",{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_instance=LoginForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            uname=data.get("username")

            pwd=data.get("password")

            print(uname,pwd)
            
            user_object=authenticate(request,username=uname,password=pwd)

            if user_object:

                login(request,user_object)


                print("user",user_object)

                return redirect("dashboard")

        

        messages.error(request,"authentification failed invalid credential")

        return render(request,"login.html",{"form":form_instance})


@method_decorator(signin_required,name="dispatch")
class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")

@method_decorator(signin_required,name="dispatch")
class DashBoardView(View):

    def get(self,request,*args, **kwargs):

        current_month=timezone.now().month

        current_year=timezone.now().year

        form_instance=SummaryForm()

        expense_list=Expense.objects.filter(user_object=request.user,created_date__month=current_month,created_date__year=current_year)

        print("expense",expense_list)

        income_list=Income.objects.filter(user_object=request.user,created_date__month=current_month,created_date__year=current_year)

        print("income",income_list)

        expense_total=expense_list.values("amount").aggregate(total=Sum("amount"))

        print("expense total",expense_total)

        income_total=income_list.values("amount").aggregate(total=Sum("amount"))

        print("income total",income_total)

        monthly_expenses={}

        monthly_incomes={}

        for month in range(1,13):

            start_date=datetime.date(current_year,month,1)

            if month==12:

                end_date=datetime.date(current_year+1,1,1)

            else:

                end_date=datetime.date(current_year,month+1,1)

            monthly_expense_total=Expense.objects.filter(user_object=request.user,created_date__gte=start_date,created_date__lte=end_date).aggregate(total=Sum('amount'))['total']

            monthly_expenses[start_date.strftime('%B')]=monthly_expense_total if monthly_expense_total else 0

            monthly_income_total=Income.objects.filter(user_object=request.user,created_date__gte=start_date,created_date__lte=end_date).aggregate(total=Sum('amount'))['total']

            monthly_incomes[start_date.strftime('%B')]=monthly_income_total if monthly_income_total else 0

        print(monthly_expenses)
        
        print(monthly_incomes)
        


        # category_summary=expense_list.values("category").annotate(total=Sum("amount"))

        # print("category summary",category_summary)

        # priority_summary=expense_list.values("priority").annotate(total=Sum("amount"))

        # print("priority_summary",priority_summary)

        # data={

        #     "expense_total":expense_total,

        #     "category_summary":category_summary,

        #     "priority_summary":priority_summary
        # }

        return render(request,"dashboard.html",{
            
            "expense":expense_total,
            "income":income_total,
            "form":form_instance,
            "monthly_incomes":monthly_incomes,
            "monthly_expenses":monthly_expenses
            }
            )

    def post(self,request,*args,**kwargs):


        form_instance=SummaryForm(request.POST)


        if form_instance.is_valid():

            data=form_instance.cleaned_data

            start_date=data.get("start_date")

            end_date=data.get("end_date")

            expense_list=Expense.objects.filter(user_object=request.user,created_date__gte=start_date,created_date__lte=end_date)

            print("expense",expense_list)

            income_list=Income.objects.filter(user_object=request.user,created_date__gte=start_date,created_date__lte=end_date)

            print("income",income_list)

            expense_total=expense_list.values("amount").aggregate(total=Sum("amount"))

            print("expense total",expense_total)

            income_total=income_list.values("amount").aggregate(total=Sum("amount"))

            print("income total",income_total)

            return render(request,"dashboard.html",{"expense":expense_total,"income":income_total,"form":form_instance})
