import json
import os

from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from .models import UserPreference, UserProfileImage
from django.contrib import messages
from django.contrib.auth.models import User
from Pivot_io import settings

from expenses.models import Expense
from income.models import Income
import requests


# Create your views here.
class PreferencesView(View):
    currency_data = []

    def load_json_data(self):
        file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

        with open(file_path, 'r') as json_file:
            json_data = json.load(json_file)

            for k, v in json_data.items():
                self.currency_data.append({'name': k, 'value': v})

    def get(self, request):

        user_image = False
        if UserProfileImage.objects.filter(user=request.user):
            user_image = True

        self.load_json_data()
        return render(request, 'preferences/index.html', context={'currency_data': self.currency_data, 'userimage': user_image})

    def post(self, request):
        # Input from the form
        new_currency = request.POST['currency']

        # User Check
        exists = UserPreference.objects.filter(user=request.user).exists()
        if exists:
            user_preferences = UserPreference.objects.get(user=request.user)

            # Old Currency Code
            old_currency = user_preferences.currency[:3]

            # Request To API
            response = requests.get(
                f'https://free.currconv.com/api/v7/convert?q={old_currency}_{new_currency[:3]}&compact=ultra&apiKey=c565e159db89deadcca6')

            # The conversion rate is returned
            # response.json returns the json format or a dict - in python
            # The key will be 'old_currency'_'new_currency' eg: USD_AUD which translates to USD to AUD

            conversion_rate = response.json()[f'{old_currency}_{new_currency[:3]}']

            # Getting all expences of a particular user
            users_expenses = Expense.objects.filter(owner=request.user)
            user_income = Income.objects.filter(owner=request.user)
            # Changing every expense to the desired format
            for expense in users_expenses:
                convert = Expense.objects.get(pk=expense.id)
                converted_amount = convert.amount * conversion_rate
                if conversion_rate < 1:
                    if converted_amount < 10:
                        convert.amount = converted_amount
                    elif 10 < converted_amount < 100:
                        convert.amount = round(converted_amount, -1)
                    elif converted_amount > 100:
                        convert.amount = round(converted_amount, -2)
                else:
                    convert.amount = round(converted_amount)
                convert.save()

            for income in user_income:
                convert = Income.objects.get(pk=income.id)
                converted_amount = convert.amount * conversion_rate
                if conversion_rate < 1:
                    if converted_amount < 10:
                        convert.amount = converted_amount
                    elif 10 < converted_amount < 100:
                        convert.amount = round(converted_amount, -1)
                    elif converted_amount > 100:
                        convert.amount = round(converted_amount, -2)
                else:
                    convert.amount = round(converted_amount)
                convert.save()

            user_preferences.currency = new_currency
            user_preferences.save()
        else:
            UserPreference.objects.create(user=request.user, currency=new_currency)
        messages.success(request, 'Changes Saved')
        return render(request, 'preferences/index.html', context={'currency_data': self.currency_data})


class UserProfile(View):
    def get(self, request):
        user = request.user
        context = {}
        try:
            user_image = UserProfileImage.objects.get(user=user)
            context = {
                'userimage': user_image
            }
        except Exception:
            print('image not found')

        return render(request, 'preferences/user_image.html', context=context)

    def post(self, request):
        selected_image = request.FILES['file']

        if UserProfileImage.objects.filter(user=request.user).exists():
            u_image = UserProfileImage.objects.get(user=request.user)
            os.remove(os.path.join(settings.BASE_DIR, f'static/img/profile/{ u_image.user_image}'))
            u_image.delete()

        u_image = UserProfileImage.objects.create(user=request.user, user_image=selected_image)
        u_image.save()
        return redirect('expenses')
