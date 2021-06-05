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

from userpreferences.models import UserPreference, UserProfileImage
from .models import Source, Income


# Create your views here.
@login_required(login_url='/authentication/login')
def index(request):
    income = Income.objects.filter(owner=request.user).order_by('-date', '-amount')
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

    paginator = Paginator(income, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user_image = False
    if UserProfileImage.objects.filter(user=request.user):
        user_image = True

    context = {
        'income': income,
        'symbol': currency_symbol,
        'pages': page_obj,
        'userimage': user_image,
    }

    return render(request, 'income/index.html', context=context)


def income_summary(request):
    # Monthly and Yearly Income

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

    current_month_data = Income.objects.filter(date__month=current_month, date__year=current_year)
    previous_month_data = Income.objects.filter(date__month=previous_month, date__year=previous_year)
    current_year_data = Income.objects.filter(date__year=current_year)
    previous_year_data = Income.objects.filter(date__year=current_year - 1)

    current_month_income = 0
    previous_month_income = 0
    current_year_income = 0
    previous_year_income = 0

    current_month_data = current_month_data.values()
    previous_month_data = previous_month_data.values()
    current_year_data = current_year_data.values()
    previous_year_data = previous_year_data.values()

    print(previous_month_data)

    for i in current_month_data:
        current_month_income += i['amount']

    for i in previous_month_data:
        previous_month_income += i['amount']

    for i in current_year_data:
        current_year_income += i['amount']

    for i in previous_year_data:
        previous_year_income += i['amount']

    user_image = False
    if UserProfileImage.objects.filter(user=request.user):
        user_image = True

    context = {
        'current_month_income': current_month_income,
        'previous_month_income': previous_month_income,
        'current_year_income': current_year_income,
        'previous_year_income': previous_year_income,
        'userimage': user_image,
    }

    return render(request, 'income/summary.html', context=context)


def delete_income(request, pk):
    try:
        income = Income.objects.get(pk=pk)
    except Exception as e:
        return render(request, 'Base/404.html')

    if not income.owner == request.user:
        return render(request, 'Base/404.html')

    income.delete()
    return redirect('income')


def edit_income(request, pk):
    try:
        income = Income.objects.get(pk=pk)
    except Exception as e:
        return render(request, 'Base/404.html')

    source = Source.objects.all()

    if request.method == 'GET':

        user_image = False
        if UserProfileImage.objects.filter(user=request.user):
            user_image = True

        context = {
            'values': income,
            'sources': source,
            'date': str(income.date),
            'userimage': user_image,
        }

        if income.owner == request.user:
            return render(request, 'income/edit_income.html', context=context)

        return render(request, 'Base/404.html')

    if request.method == 'POST':
        context = {
            'categories': source,
            'values': request.POST
        }
        amount = request.POST['amount']
        if not amount:
            amount = income.amount

        selected_category = request.POST['source']
        if selected_category == '--Select--':
            selected_category = income.category

        date = request.POST['expense_date']
        if not date:
            date = income.date
        description = request.POST['description']

        income.amount = amount
        income.date = date
        income.description = description
        income.category = selected_category
        income.save()

        messages.success(request, 'Expense was successfully modified')
        return redirect('income')


def search_income(request):
    print('get')
    if request.method == 'POST':
        search_string = json.loads(request.body).get('search_value')

        income = Income.objects.filter(amount__istartswith=search_string, owner=request.user) | \
                 Income.objects.filter(date__istartswith=search_string, owner=request.user) | \
                 Income.objects.filter(description__icontains=search_string, owner=request.user) | \
                 Income.objects.filter(source__icontains=search_string, owner=request.user)
        expense_data = income.values()

        return JsonResponse(list(expense_data), safe=False)


class Add_Income(View):
    def get(self, request):
        source = Source.objects.all()

        user_image = False
        if UserProfileImage.objects.filter(user=request.user):
            user_image = True

        context = {
            'source': source,
            'userimage': user_image,
        }
        return render(request, 'income/add_income.html', context=context)

    def post(self, request):
        source = Source.objects.all()
        context = {
            'categories': source,
            'values': request.POST,
        }
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', context=context)

        selected_source = request.POST['source']
        if selected_source == '--Select--':
            messages.error(request, 'You must select a category')
            return render(request, 'income/add_income.html', context=context)

        date = request.POST['income_date']
        if not date:
            messages.error(request, 'You must select a date')
            return render(request, 'income/add_income.html', context=context)
        description = request.POST['description']

        Income.objects.create(amount=amount, date=date, description=description, owner=request.user,
                              source=selected_source)
        messages.success(request, 'Expense was successfully added')
        return redirect('income')


def Chart(request):
    income = Income.objects.filter(owner=request.user)
    income_data = income.values()
    return JsonResponse(list(income_data), safe=False)
