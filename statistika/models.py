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
    type = models.ManyToManyField(BusinessType, blank=False)
    join_date = models.DateField(auto_now_add=True)
    created_date = models.DateField(auto_now_add=False, null=True, blank=True)
    employees = models.IntegerField(default=0)
    deleted = models.BooleanField(default=False)
    
    def delete(self):
        self.deleted = True
        return self.deleted

OYLIK, XAFTALIK = (
    "30",
    "7"
)

ADDED, STOPPED, DELETED = (
    "Added",
    "Stopped",
    "Deleted"
)

class Income(models.Model):
    TIME_CHOISE = (
        (OYLIK, OYLIK),
        (XAFTALIK, XAFTALIK)
    )
    
    STATUS_CHOISE = (
        (ADDED, ADDED),
        (STOPPED, STOPPED),
        (DELETED, DELETED)
    )
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    from_what = models.CharField(max_length=250, null=True)
    cost = models.IntegerField(default=0)
    auto = models.BooleanField(default=False)
    often = models.CharField(max_length=25, choices=TIME_CHOISE, null=True, blank=True)
    status = models.CharField(max_length=25, choices=STATUS_CHOISE, null=True, blank=True)
    next_pay = models.DateField(null=True, blank=True)


class Expense(models.Model):
    TIME_CHOISE = (
        (OYLIK, OYLIK),
        (XAFTALIK, XAFTALIK)
    )

    STATUS_CHOISE = (
        (ADDED, ADDED),
        (STOPPED, STOPPED),
        (DELETED, DELETED)
    )

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    from_what = models.CharField(max_length=250, null=True)
    cost = models.IntegerField(default=0)
    auto = models.BooleanField(default=False)
    often = models.CharField(max_length=25, choices=TIME_CHOISE, null=True, blank=True)
    status = models.CharField(max_length=25, choices=STATUS_CHOISE, null=True, blank=True)
    next_pay = models.DateField(null=True, blank=True)
