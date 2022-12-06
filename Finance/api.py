from rest_framework import routers
from statistika.views import *

router = routers.DefaultRouter()

router.register(r'companies', CompanyView, basename='companies')
router.register(r'incomes', IncomeView, basename='incomes')
router.register(r'expenses', ExpanseView, basename='expenses')
router.register(r'incomes_by_company', IncomeByCompany, basename='incomes_by_company')
router.register(r'expenses_by_company', ExpenseByCompany, basename='expenses_by_company')
router.register(r'email_check', ManagerEmailCheck, basename='email_check')

