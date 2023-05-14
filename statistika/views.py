from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import *
import pandas as pd
from authentication.models import FinUser as Manager
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import HttpResponse, FileResponse
from django.db.models import Q
from pathlib import Path


class CompanyView(generics.ListCreateAPIView):
    queryset = Company.objects.filter(deleted=False).all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            user = request.user
            objects = self.queryset.filter(manager_id=user.id).all()
            serializer = self.get_serializer(objects, many=True)
            return Response(serializer.data)
        except Exception as exx:
            return Response({"Error": str(exx)})

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
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
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        company_id = kwargs['pk']
        company = self.queryset.filter(id=company_id).first()
        if company:
            try:
                user = request.user
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
                user = request.user
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
                user = request.user
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
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Income.objects.all()
        company_id = self.request.query_params.get('company_id')
        if company_id is not None:
            queryset = queryset.filter(company_id=company_id)
        return queryset

    def list(self, request, *args, **kwargs):
        company_id = request.GET.get('company_id')
        if company_id is not None:
            try:
                company = Company.objects.filter(id=company_id).first()
                if company:
                    user = request.user
                    manager = company.manager.id
                    if manager == user.id:
                        incoms = self.get_queryset()
                        dates = []
                        response_data = []
                        for income in incoms:
                            dates.append((income.date.year, income.date.month))
                        dates = list(dict.fromkeys(dates))
                        for date in dates:
                            incs = Income.objects.filter(company_id=company_id, date__year=date[0], date__month=date[1]).values('cost').all()
                            sums = [income['cost'] for income in incs]
                            incomes_by_moth = {
                                'month': f'{date[0]}/{date[1]}',
                                'summa': sum(sums)
                            }
                            response_data.append(incomes_by_moth)                            
                        serializer = self.get_serializer(incoms, many=True)
                        return Response(response_data)
                    else:
                        return Response({"Error": "Authentification failed"}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return super().list(request, *args, **kwargs)
            except Exception as exx:
                return Response({"Error": str(exx)})
        else:
            return super().list(request, *args, **kwargs)
        
        
    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            company_id = request.data["company"]
            company = Company.objects.get(id=company_id)
            if company.manager.id == user.id:
                return super().create(request, *args, **kwargs)
            else:
                return Response({"Error": "Authentification failed"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as exx:
            return Response({"Error": str(exx)})


class ExpenseView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Expense.objects.all()
        company_id = self.request.query_params.get('company_id')
        if company_id is not None:
            queryset = queryset.filter(company_id=company_id)
        return queryset

    def list(self, request, *args, **kwargs):
        company_id = request.GET.get('company_id')
        if company_id is not None:
            try:
                company = Company.objects.filter(id=company_id).first()
                if company:
                    user = request.user
                    manager = company.manager.id
                    if manager == user.id:
                        expenses = self.get_queryset()
                        dates = []
                        response_data = []
                        expenses_by_moth = {}
                        for income in expenses:
                            dates.append((income.date.year, income.date.month))
                        dates = list(dict.fromkeys(dates))
                        for date in dates:
                            exps = Expense.objects.filter(company_id=company_id, date__year=date[0], date__month=date[1]).values('cost').all()
                            sums = [expense['cost'] for expense in exps]
                            expenses_by_moth = {
                                'month': f'{date[0]}/{date[1]}',
                                'summa': sum(sums)
                            }
                        return Response(response_data)
                    else:
                        return Response({"Error": "Authentification failed"}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return super().list(request, *args, **kwargs)
            except Exception as exx:
                return Response({"Error": str(exx)})
        else:
            return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
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
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            user = request.user
            company_id = request.data["company"]
            company = Company.objects.get(id=company_id)
            if company.manager.id == user.id:
                begin = request.data["begin"]
                end = request.data["end"]
                datas = Income.objects.values().filter(Q(date__gte=begin) & Q(date__lte=end), company__id=company_id)
                return Response(datas.values())
            else:
                return Response({"Error": "Authentification failed"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as exx:
            return Response({"Error": str(exx)})


class ExpenseByDateView(generics.CreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseByDateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            user = request.user
            company_id = request.data["company"]
            company = Company.objects.get(id=company_id)
            if company.manager.id == user.id:
                begin = request.data["begin"]
                end = request.data["end"]
                datas = Expense.objects.values().filter(Q(date__gte=begin) & Q(date__lte=end), company__id=company_id)
                return Response(datas.values())
            else:
                return Response({"Error": "Authentification failed"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as exx:
            return Response({"Error": str(exx)})


class GetExpenseDocumentView(generics.CreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseByDateSerializer

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            company_id = request.data["company"]
            company = Company.objects.get(id=company_id)
            if company.manager.id == user.id:
                begin = request.data["begin"]
                end = request.data["end"]
                from_whats = []
                summas = []
                dates = []
                datas = Expense.objects.filter(Q(date__gte=begin) & Q(date__lte=end), company__id=company_id)
                datas = Expense.objects.all()
                for expense in datas:
                    dates.append(expense.date)
                    summas.append(expense.cost)
                    from_whats.append(expense.from_what)
                df = pd.DataFrame({'Sana': dates,
                                   'Nima uchun': from_whats,
                                   'Summa': summas})
                file_path = Path('./files/xisobot.xlsx')
                df.to_excel(file_path, )
                return Response({'status':'ok', 'file': "http://185.65.202.40:2843/files/xisobot.xlsx"})
            else:
                return Response({"Error": "Authentification failed"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as exx:
            return Response({"Error": str(exx)})


class GetIncomeDocumentView(generics.CreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeByDateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            company_id = request.data["company"]
            company = Company.objects.get(id=company_id)
            if company.manager.id == user.id:
                begin = request.data["begin"]
                end = request.data["end"]
                from_whats = []
                summas = []
                dates = []
                datas = Income.objects.filter(Q(date__gte=begin) & Q(date__lte=end), company__id=company_id)
                datas = Income.objects.all()
                for income in datas:
                    dates.append(income.date)
                    summas.append(income.cost)
                    from_whats.append(income.from_what)
                df = pd.DataFrame({'Sana': dates,
                                   'Nima uchun': from_whats,
                                   'Summa': summas})
                df.to_excel('./files/xisobot.xlsx')
                
                return Response({'status':'ok', 'file': "http://185.65.202.40:2843/files/xisobot.xlsx"})
            else:
                return Response({"Error": "Authentification failed"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as exx:
            return Response({"Error": str(exx)})


class TestView(generics.ListCreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get(self, request, *args, **kwargs):
        print(request.user)
        return super().get(request, *args, **kwargs)


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


class CategoryView(generics.ListCreateAPIView):
    queryset = BusinessCategory.objects.all()
    serializer_class = CategorySerializer


class TypeView(generics.ListCreateAPIView):
    serializer_class = TypeSerializer

    def get_queryset(self):
        queryset = BusinessType.objects.all()
        category_id = self.request.query_params.get('category_id')
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        return queryset
