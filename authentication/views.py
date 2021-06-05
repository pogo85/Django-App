from django.shortcuts import render, redirect, reverse
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage

# encoding imports
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

# Login
from django.contrib import auth

# token generator in custom utils
from .utils import token_generator
from django.contrib.auth.tokens import PasswordResetTokenGenerator

import json

# multithreading
import threading

# constants
NUMS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


# Multithreading Class
class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


# Create your views here.
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'field_values': request.POST
        }

        if username == '' or email == '' or password == '':
            messages.error(request, 'All fields are required')
            return render(request, 'authentication/register.html', context)

        if len(password) < 6:
            messages.error(request, 'password must be at least 6 characters')
            return render(request, 'authentication/register.html', context)

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                user = User.objects.create(username=username, email=email)
                user.set_password(password)
                user.is_active = True
                user.save()

                current_site = get_current_site(request)

                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': token_generator.make_token(user)
                }
                link = reverse('activate', kwargs={'user_idb64': email_body['uid'], 'token': email_body['token']})

                activate_url = 'http://' + current_site.domain + link

                email_subject = 'Account Activation Email'
                email = EmailMessage(
                    email_subject,
                    f'Hi {user.username}, please use this link to verify your account \n {activate_url}',
                    'pivot_activator@gmail.com',
                    [email],
                )
                # EmailThread(email).start()
                messages.success(request, 'Account successfully created, Check your email')

        return render(request, 'authentication/register.html')


class LogoutView(View):
    def get(self, request):
        pass

    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have successfully been logged out')
        return redirect('login_view')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(request, username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, f'Welcome {user.username}.')
                    return redirect('expenses')
                messages.error(request, f'{user.username} is not active.')
                return render(request, 'authentication/login.html')
            messages.error(request, f'Account {username} does not exist')
            return render(request, 'authentication/login.html')
        messages.error(request, f'Please fill all fields')
        return render(request, 'authentication/login.html')


class VerificationView(View):
    def get(self, request, user_idb64, token):

        try:
            pk = force_text(urlsafe_base64_decode(user_idb64))
            user = User.objects.get(id=pk)

            if not token_generator.check_token(user, token):
                return redirect('login_view' + '?message=' + 'User already activated')
            else:
                print('No')
            if user.is_active:
                return redirect('login_view')
            user.is_active = True
            user.save()
            messages.success(request, 'Account activated successfully')
            return redirect('login_view')

        except Exception as ex:
            pass
        return redirect('login_view')


class UsernameValidationView(View):
    def get(self, request):
        return render(request, 'Base/404.html')

    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only be alphanumeric'}, status=400)
        if username[0] in NUMS:
            return JsonResponse({'username_number': 'username should not start with a number'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_already_exists': 'username taken, choose a different username'}, status=400)
        return JsonResponse({'username_valid': True})


class EmailValidationView(View):
    def get(self, request):
        return render(request, 'Base/404.html')

    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Email invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_already_exists': 'email taken, choose a different email'}, status=400)
        return JsonResponse({'email_valid': True})


class RequestPasswordReset(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')

    def post(self, request):
        email = request.POST['email']

        context = {
            'field_values': request.POST
        }

        if not validate_email(email):
            messages.error(request, 'Please enter a valid email')
            return render(request, 'authentication/reset-password.html', context=context)

        current_site = get_current_site(request)
        user = User.objects.filter(email=email)
        if user.exists():
            email_contents = {
                'user': user[0],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0])
            }
            link = reverse('reset-user-password',
                           kwargs={'user_idb64': email_contents['uid'], 'token': email_contents['token']})

            reset_url = 'http://' + current_site.domain + link

            email_subject = 'Password Reset Instructions'
            email = EmailMessage(
                email_subject,
                f'Hi {user[0].username}, please use this link to reset your password \n {reset_url}',
                'pivot_activator@gmail.com',
                [email],
            )
            EmailThread(email).start()

        messages.success(request, 'We have sent you an email')
        return render(request, 'authentication/reset-password.html')


class ValidateResetEmail(View):
    def get(self, request):
        return render(request, 'Base/404.html')

    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Email invalid'}, status=400)
        return JsonResponse({'email_valid': True})


class ResetUserPassword(View):
    def get(self, request, user_idb64, token):
        context = {
            'user_idb64': user_idb64,
            'token': token
        }

        try:
            user_id = force_text(urlsafe_base64_decode(user_idb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, 'Password Reset Link is invalid, request a new one')
                return render(request, 'authentication/reset-password.html')
        except Exception:
            pass
        return render(request, 'authentication/set-new-password.html', context=context)

    def post(self, request, user_idb64, token):

        password = request.POST['password']
        context = {
            'user_idb64': user_idb64,
            'token': token
        }
        try:
            user_id = force_text(urlsafe_base64_decode(user_idb64))
            user = User.objects.get(id=user_id)
            user.set_password(password)
            user.save()
            messages.success(request, "Password has been reset successfully")
            return render(request, 'authentication/login.html')
        except Exception:
            messages.error(request, "Something has gone wrong")
            return render(request, 'authentication/set-new-password.html', context=context)
