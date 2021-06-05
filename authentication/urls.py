from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('login', LoginView.as_view(), name='login_view'),
    path('logout', LogoutView.as_view(), name='logout_view'),
    path('register', RegistrationView.as_view(), name='registration_view'),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name='validate-username'),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name='validate-email'),
    path('activate/<user_idb64>/<token>', VerificationView.as_view(), name='activate'),
    path('request-reset-link', RequestPasswordReset.as_view(), name='request-reset-link'),
    path('validate-reset-email', csrf_exempt(ValidateResetEmail.as_view()), name='validate-reset-email'),
    path('reset-user-password/<user_idb64>/<token>', ResetUserPassword.as_view(), name='reset-user-password'),
]
