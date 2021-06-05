from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', views.index, name='income'),
    path('add_income', views.Add_Income.as_view(), name='add_income'),
    path('edit_income/<int:pk>', views.edit_income, name='edit_income'),
    path('delete_income/<int:pk>', views.delete_income, name='delete_income'),
    path('search_income', csrf_exempt(views.search_income), name='search_income'),
    path('Chart', csrf_exempt(views.Chart), name='income_chart'),
    path('sumary', views.income_summary, name='income_summary'),
]
