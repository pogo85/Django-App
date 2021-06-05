from django.urls import path
from . import views

urlpatterns = [
    path('', views.PreferencesView.as_view(), name='preferences'),
    path('set-profile-picture', views.UserProfile.as_view(), name='set-profile-picture'),
]
