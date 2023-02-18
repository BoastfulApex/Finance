from rest_framework import serializers
from .models import *
from .models import Manager as User


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = "__all__"


class IncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Income
        fields = "__all__"


class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense
        fields = "__all__"


class IncomeByDateSerializer(serializers.Serializer):
    begin = serializers.DateField()
    end = serializers.DateField()
    company = serializers.CharField()


class ExpenseByDateSerializer(serializers.Serializer):
    begin = serializers.DateField()
    end = serializers.DateField()
    company = serializers.CharField()

