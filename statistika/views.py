from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import viewsets
from .serializers import *
import smtplib, ssl
from .generator import generate_random_password
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from authentication.models import FinUser as Manager


class CompanyView(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class IncomeView(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer


class ExpanseView(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


class IncomeByCompany(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

    def retrieve(self, request, *args, **kwargs):
        company_id = kwargs['pk']
        incomes = self.queryset.filter(company_id=company_id)
        serializer = self.get_serializer(incomes, many=True)
        return Response(serializer.data)


class ExpenseByCompany(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def retrieve(self, request, *args, **kwargs):
        company_id = kwargs['pk']
        incomes = self.queryset.filter(company_id=company_id)
        serializer = self.get_serializer(incomes, many=True)
        return Response(serializer.data)


class ManagerEmailCheck(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ExpenseSerializer

    def retrieve(self, request, *args, **kwargs):
        manager_id = kwargs['pk']
        manager = Manager.objects.get(id=manager_id)
        m_email = manager.email
        if manager.email_check:
            return Response({"Email was checked"})
        else:
            check_pass = generate_random_password()
            sender_address = 'forbot2503@gmail.com'
            sender_pass = 'Wertus89'
            message = MIMEMultipart()
            body = f'{check_pass}'
            message['From'] = sender_address
            message['To'] = m_email
            message['Subject'] = 'Email tekshiruvi'
            message.attach(MIMEText(body, "plain"))
            session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
            session.starttls()  # enable security
            session.login(sender_address, sender_pass)  # login with mail_id and password
            text = message.as_string()
            session.sendmail(sender_address, m_email, text)
            session.quit()
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_address, sender_pass)
                server.sendmail(sender_address, m_email, text)
            return Response({"Email check password": check_pass})
