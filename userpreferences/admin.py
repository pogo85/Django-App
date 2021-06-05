from django.contrib import admin
from . models import UserPreference, UserProfileImage

# Register your models here.
admin.site.register(UserPreference)
admin.site.register(UserProfileImage)
