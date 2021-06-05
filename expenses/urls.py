from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', views.index, name='expenses'),
    path('add_expense', views.Add_Expense.as_view(), name='add_expense'),
    path('edit_expense/<int:pk>', views.edit_expense, name='edit_expense'),
    path('delete_expense/<int:pk>', views.delete_expense, name='delete_expense'),
    path('search_expenses', csrf_exempt(views.search_expense), name='search_expense'),
    path('Chart', csrf_exempt(views.Chart), name='expense_chart'),
    path('summary', views.expense_summary, name='expense_summary'),
]
