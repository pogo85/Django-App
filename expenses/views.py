import json
import os
import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse

from userpreferences.models import UserPreference
from .models import Category, Expense
from userpreferences.models import UserProfileImage


# Create your views here.
@login_required(login_url='/authentication/login')
def index(request):
    expenses = Expense.objects.filter(owner=request.user).order_by('-date', '-amount')
    preference = UserPreference.objects.filter(user=request.user)
    if preference:
        preference = UserPreference.objects.get(user=request.user)
        currency_code = preference.currency[:3]
    else:
        UserPreference.objects.create(user=request.user, currency='INR - Indian Rupee')
        preference = UserPreference.objects.get(user=request.user)
        currency_code = preference.currency[:3]

    file_path = os.path.join(settings.BASE_DIR, 'currency_symbol.json')
    with open(file_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        currency_symbol = json_data[currency_code]['symbol']

    paginator = Paginator(expenses, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user_image = False

    if UserProfileImage.objects.filter(user=request.user):
        user_image = True

    context = {
        'expenses': expenses,
        'symbol': currency_symbol,
        'pages': page_obj,
        'userimage': user_image,
    }

    return render(request, 'expenses/index.html', context=context)


def expense_summary(request):
    # Monthly and Yearly Expense

    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year

    previous_month = 0
    previous_year = 0

    if current_month == 1:
        previous_month = 12
        previous_year = current_year - 1
    else:
        previous_month = current_month - 1
        previous_year = current_year

    current_month_data = Expense.objects.filter(date__month=current_month, date__year=current_year)
    previous_month_data = Expense.objects.filter(date__month=previous_month, date__year=previous_year)
    current_year_data = Expense.objects.filter(date__year=current_year)
    previous_year_data = Expense.objects.filter(date__year=current_year - 1)

    current_month_expense = 0
    previous_month_expense = 0
    current_year_expense = 0
    previous_year_expense = 0

    current_month_data = current_month_data.values()
    previous_month_data = previous_month_data.values()
    current_year_data = current_year_data.values()
    previous_year_data = previous_year_data.values()

    print(previous_month_data)

    for i in current_month_data:
        current_month_expense += i['amount']

    for i in previous_month_data:
        previous_month_expense += i['amount']

    for i in current_year_data:
        current_year_expense += i['amount']

    for i in previous_year_data:
        previous_year_expense += i['amount']

    user_image = False
    if UserProfileImage.objects.filter(user=request.user):
        user_image = True

    context = {
        'current_month_income': current_month_expense,
        'previous_month_income': previous_month_expense,
        'current_year_income': current_year_expense,
        'previous_year_income': previous_year_expense,
        'userimage': user_image,
    }

    return render(request, 'expenses/summary.html', context=context)


def delete_expense(request, pk):
    try:
        expense = Expense.objects.get(pk=pk)
    except Exception as e:
        return render(request, 'Base/404.html')

    if not expense.owner == request.user:
        return render(request, 'Base/404.html')

    expense.delete()
    return redirect('expenses')


def edit_expense(request, pk):
    try:
        expense = Expense.objects.get(pk=pk)
    except Exception as e:
        return render(request, 'Base/404.html')

    category = Category.objects.all()

    if request.method == 'GET':

        user_image = False
        if UserProfileImage.objects.filter(user=request.user):
            user_image = True

        context = {
            'values': expense,
            'categories': category,
            'date': str(expense.date),
            'userimage': user_image,
        }

        if expense.owner == request.user:
            return render(request, 'expenses/edit_expense.html', context=context)

        return render(request, 'Base/404.html')

    if request.method == 'POST':
        context = {
            'categories': category,
            'values': request.POST
        }
        amount = request.POST['amount']
        if not amount:
            amount = expense.amount

        selected_category = request.POST['category']
        if selected_category == '--Select--':
            selected_category = expense.category

        date = request.POST['expense_date']
        if not date:
            date = expense.date
        description = request.POST['description']

        expense.amount = amount
        expense.date = date
        expense.description = description
        expense.category = selected_category
        expense.save()

        messages.success(request, 'Expense was successfully modified')
        return redirect('expenses')


def search_expense(request):
    if request.method == 'POST':
        search_string = json.loads(request.body).get('search_value')

        expenses = Expense.objects.filter(amount__istartswith=search_string, owner=request.user) | \
                   Expense.objects.filter(date__istartswith=search_string, owner=request.user) | \
                   Expense.objects.filter(description__icontains=search_string, owner=request.user) | \
                   Expense.objects.filter(category__icontains=search_string, owner=request.user)
        expense_data = expenses.values()

        return JsonResponse(list(expense_data), safe=False)


class Add_Expense(View):
    def get(self, request):
        category = Category.objects.all()

        user_image = False
        if UserProfileImage.objects.filter(user=request.user):
            user_image = True

        context = {
            'categories': category,
            'userimage': user_image,
        }
        return render(request, 'expenses/add_expense.html', context=context)

    def post(self, request):
        category = Category.objects.all()

        context = {
            'categories': category,
            'values': request.POST,
        }
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context=context)

        selected_category = request.POST['category']
        if selected_category == '--Select--':
            messages.error(request, 'You must select a category')
            return render(request, 'expenses/add_expense.html', context=context)

        date = request.POST['expense_date']
        if not date:
            messages.error(request, 'You must select a date')
            return render(request, 'expenses/add_expense.html', context=context)
        description = request.POST['description']

        Expense.objects.create(amount=amount, date=date, description=description, owner=request.user,
                               category=selected_category)
        messages.success(request, 'Expense was successfully added')
        return redirect('expenses')


def Chart(request):
    expenses = Expense.objects.filter(owner=request.user)
    expense_data = expenses.values()
    return JsonResponse(list(expense_data), safe=False)
