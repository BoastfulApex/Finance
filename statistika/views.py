from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import viewsets
from .serializers import *
import smtplib, ssl
from .generator import generate_random_password
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from authentication.models import FinUser as Manager
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import HttpResponse
from django.db.models import Q

class CompanyView(generics.ListCreateAPIView):
    queryset = Company.objects.filter(deleted=False).all()
    serializer_class = CompanySerializer
    
    def list(self, request, *args, **kwargs):
        try:
            jwt_object = JWTAuthentication() 
            validated_token = jwt_object.get_validated_token(request.headers['token'])
            user = jwt_object.get_user(validated_token)
            objects = self.queryset.filter(manager_id=user.id).all()
            serializer = self.get_serializer(objects, many=True)
            return Response(serializer.data)                
        
        except Exception as exx:
            return Response({"Error": str(exx)})

    def create(self, request, *args, **kwargs):
        try:
            jwt_object = JWTAuthentication() 
            validated_token = jwt_object.get_validated_token(request.headers['token'])
            user = jwt_object.get_user(validated_token)
            manager = request.data["manager"]
            if manager == user.id:
                return super().create(request, *args, **kwargs)
            else:
                return Response({"Error": "Authentification failed"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as exx:
            return Response({"Error": str(exx)})


class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.filter(deleted=False).all()
    serializer_class = CompanySerializer
    
    def retrieve(self, request, *args, **kwargs):
        company_id = kwargs['pk']
        company = self.queryset.filter(id=company_id).first()
        if company:
            try:
                jwt_object = JWTAuthentication() 
                validated_token = jwt_object.get_validated_token(request.headers['token'])
                user = jwt_object.get_user(validated_token)
                manager = company.manager.id
                if manager == user.id:
                    return super().retrieve(request, *args, **kwargs)
                else:
                    return Response({"Error": "Authentification failed"}, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as exx:
                return Response({"Error": str(exx)})
        else:
            return Response({"status": "not found"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        company_id = kwargs['pk']
        company = self.queryset.filter(id=company_id).first()
        if company:
            try:
                jwt_object = JWTAuthentication() 
                validated_token = jwt_object.get_validated_token(request.headers['token'])
                user = jwt_object.get_user(validated_token)
                manager = company.manager.id
                if manager == user.id:
                    if 'name' in request.data:
                        company.name = request.data["name"]
                    if 'employees' in request.data:
                        company.employees = int(request.data["employees"])
                    if 'category' in request.data:
                        category = BusinessCategory.ojects.get(id=request.data["category"])
                        company.category = category
                    company.save()
                    return Response({"status": "updated"})
                else:
                    return Response({"Error": "Authentification failed"}, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as exx:
                return Response({"Error": str(exx)})
        else:
            return Response({"status": "not found"}, status=status.HTTP_404_NOT_FOUND)
        

    def destroy(self, request, *args, **kwargs):
        company_id = kwargs['pk']
        company = self.queryset.filter(id=company_id).first()
        if company:
            try:
                jwt_object = JWTAuthentication() 
                validated_token = jwt_object.get_validated_token(request.headers['token'])
                user = jwt_object.get_user(validated_token)
                manager = company.manager.id
                if manager == user.id:
                    company.deleteCompany()
                    company.save()
                    return Response({"status": "deleted"})
                else:
                    return Response({"Error": "Authentification failed"}, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as exx:
                return Response({"Error": str(exx)})
        else:
            return Response({"status": "not found"}, status=status.HTTP_404_NOT_FOUND)
        

class IncomeView(generics.ListCreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

    def list(self, request, *args, **kwargs):
        company_id = request.GET.get('company_id')
        if company_id:
            try:
                company = Company.objects.filter(id=company_id).first()
                if company:
                    jwt_object = JWTAuthentication()
                    validated_token = jwt_object.get_validated_token(request.headers['token'])
                    user = jwt_object.get_user(validated_token)
                    manager = company.manager.id
                    if manager == user.id:
                        incoms = self.queryset.filter(company__id=company_id).all()
                        serializer = self.get_serializer(incoms, many=True)
                        return Response(serializer.data)
                    else:
                        return Response({"Error": "Authentification failed"}, status=status.HTTP_401_UNAUTHORIZED)                    
                else:
                    return Response({"status": "not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as exx:
                return Response({"Error": str(exx)})
        else:
            return HttpResponse()

    def create(self, request, *args, **kwargs):
        try:
            jwt_object = JWTAuthentication() 
            validated_token = jwt_object.get_validated_token(request.headers['token'])
            user = jwt_object.get_user(validated_token)
            company_id = request.data["company"]
            company = Company.objects.get(id=company_id)
            if company.manager.id == user.id:
                return super().create(request, *args, **kwargs)
            else:
                return Response({"Error": "Authentification failed"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as exx:
            return Response({"Error": str(exx)})
                

class ExpenseView(generics.ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def list(self, request, *args, **kwargs):
        company_id = request.GET.get('company_id')
        if company_id:
            try:
                company = Company.objects.filter(id=company_id).first()
                if company:
                    jwt_object = JWTAuthentication()
                    validated_token = jwt_object.get_validated_token(request.headers['token'])
                    user = jwt_object.get_user(validated_token)
                    manager = company.manager.id
                    if manager == user.id:
                        incoms = self.queryset.filter(company__id=company_id).all()
                        serializer = self.get_serializer(incoms, many=True)
                        return Response(serializer.data)
                    else:
                        return Response({"Error": "Authentification failed"}, status=status.HTTP_401_UNAUTHORIZED)                    
                else:
                    return Response({"status": "not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as exx:
                return Response({"Error": str(exx)})
        else:
            return HttpResponse()

    def create(self, request, *args, **kwargs):
        try:
            jwt_object = JWTAuthentication() 
            validated_token = jwt_object.get_validated_token(request.headers['token'])
            user = jwt_object.get_user(validated_token)
            company_id = request.data["company"]
            company = Company.objects.get(id=company_id)
            if company.manager.id == user.id:
                return super().create(request, *args, **kwargs)
            else:
                return Response({"Error": "Authentification failed"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as exx:
            return Response({"Error": str(exx)})


class IncomeByDateView(generics.CreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeByDateSerializer

    def create(self, request, *args, **kwargs):
        try:
            jwt_object = JWTAuthentication() 
            validated_token = jwt_object.get_validated_token(request.headers['token'])
            user = jwt_object.get_user(validated_token)
            company_id = request.data["company"]
            company = Company.objects.get(id=company_id)
            if company.manager.id == user.id:
                begin = request.data["begin"]
                end = request.data["end"]
                datas = Income.objects.values().filter(Q(date__gte=begin)&Q(date__lte=end), company__id=company_id)
                return Response(datas.values())
            else:
                return Response({"Error": "Authentification failed"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as exx:
            return Response({"Error": str(exx)})


class ManagerEmailCheck(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ExpenseSerializer

    # def retrieve(self, request, *args, **kwargs):
    #     manager_id = kwargs['pk']
    #     manager = Manager.objects.get(id=manager_id)
    #     m_email = manager.email
    #     if manager.email_check:
    #         return Response({"Email was checked"})
    #     else:
    #         check_pass = generate_random_password()
    #         sender_address = 'forbot2503@gmail.com'
    #         sender_pass = 'Wertus89'
    #         message = MIMEMultipart()
    #         body = f'{check_pass}'
    #         message['From'] = sender_address
    #         message['To'] = m_email
    #         message['Subject'] = 'Email tekshiruvi'
    #         message.attach(MIMEText(body, "plain"))
    #         session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    #         session.starttls()  # enable security
    #         session.login(sender_address, sender_pass)  # login with mail_id and password
    #         text = message.as_string()
    #         session.sendmail(sender_address, m_email, text)
    #         session.quit()
    #         context = ssl.create_default_context()
    #         with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    #             server.login(sender_address, sender_pass)
    #             server.sendmail(sender_address, m_email, text)
    #         return Response({"Email check password": check_pass})
