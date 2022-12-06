from django.db import models
from authentication.models import FinUser as Manager


class BusinessCategory(models.Model):
    business_category = models.CharField(max_length=250, null=True)
    
    def __str__(self):
        return self.business_category


class BusinessType(models.Model):
    business_type = models.CharField(max_length=250, null=True)
    category = models.ForeignKey(BusinessCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.business_type


class Company(models.Model):
    name = models.CharField(max_length=250, null=True)
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(BusinessCategory, on_delete=models.SET_NULL, null=True)
    type = models.ManyToManyField(BusinessType)
    join_date = models.DateField(auto_now_add=True)
    created_date = models.DateField(auto_now_add=False, null=True, blank=True)
    employees = models.IntegerField(default=0)


class Income(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    from_what = models.CharField(max_length=250, null=True)
    cost = models.IntegerField(default=0)
    auto = models.BooleanField(default=False)


class Expense(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    from_what = models.CharField(max_length=250, null=True)
    cost = models.IntegerField(default=0)
    auto = models.BooleanField(default=False)
