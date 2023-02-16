from django.urls import path
from .views import *

urlpatterns = [
    path('company/', CompanyView.as_view(), name='company'),
    path('company/<int:pk>', CompanyDetail.as_view(), name='company'),
    path('income/', IncomeView.as_view(), name='income'),
    path('expense/', ExpenseView.as_view(), name='expense'),
    path('income_by_date/', IncomeByDateView.as_view(), name='income_by_date'),
]
