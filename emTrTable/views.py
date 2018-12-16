from django.shortcuts import render, redirect
from .models import EmployeeTreeModel
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.http import JsonResponse
from rest_framework import viewsets
from emTrTable.mySerializers import EmployeeSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication






class EmployeeForm(forms.ModelForm):
    use_required_attribute = True
    photo = forms.ImageField(required=False)
    class Meta:
        model = EmployeeTreeModel
        fields = ['fullName', 'position', 'photo', 'salary', 'employeeDate', 'bossID', 'level', 'id','bossName']

class EmployeeViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    queryset = EmployeeTreeModel.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]


    @action(detail=False)
    def searchByfield(self, request):
        options = dict(request.GET)
        for opt in options:
            options[opt] = options[opt][0]
        filtered = self.queryset.filter(**options)
        serialized = self.serializer_class(filtered, many=True)
        return Response(serialized.data)

def index(request):
    if request.user.is_authenticated:
        return render(request, 'emploeeTreeTable.html')
    else:
        return redirect('auth/login')

def getjsonTable(request):
    if request.user.is_authenticated:
        employees = EmployeeTreeModel.objects.all().filter(level__lte=4).order_by('fullName')
        response_data = EmployeeSerializer(employees, many=True).data

        return JsonResponse({'table':response_data}, safe=True)
    else:
        return redirect('auth/login')

def getTableByBossId(request):
    if request.user.is_authenticated:
        bossID = request.GET.get('bossID')
        order_by = request.GET.get('order_by') if request.GET.get('order_by') != '' else 'fullName'
        employees = EmployeeTreeModel.objects.all().filter(bossID=bossID).order_by(order_by)
        response_data = EmployeeSerializer(employees, many=True).data
        return JsonResponse({'table':response_data})
    else:
        return redirect('auth/login')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            #user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def logiView(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        redirect('')


def serchby(request):
    if request.user.is_authenticated:
        options = dict(request.GET)
        for opt in options:
            options[opt] = options[opt][0]
        responded = EmployeeTreeModel.objects.filter(**options)
        serialized = EmployeeSerializer(responded, many=True)
        return JsonResponse({'table':serialized.data})
    else:
        return redirect('auth/login')

def detailPage(request):
    if request.user.is_authenticated:
        pageID = request.GET.get('ID')
        article = EmployeeTreeModel.objects.get(pk=pageID)
        if int(pageID) > 1:
            bosses = EmployeeTreeModel.objects.all().filter(level__lt=5)
        else:
            bosses = 'False'
        if request.method == 'POST':
            form = EmployeeForm(request.POST, request.FILES, instance=article)
            if form.is_valid():
                form.save()
                return redirect('/detailPage?ID='+str(article.id))
        else:


            form = EmployeeForm(instance=article)

            return render(request, 'detailPage.html', {'form': form, 'bossList':bosses})

