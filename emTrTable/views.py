from django.shortcuts import render, HttpResponse, redirect, render_to_response
from .models import EmployeeTreeModel
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.http import JsonResponse





class EmployeeForm(forms.ModelForm):
    use_required_attribute = True
    photo = forms.ImageField(required=False)
    class Meta:
        model = EmployeeTreeModel
        fields = ['fullName', 'position', 'photo', 'salary', 'employeeDate', 'bossID', 'level', 'id']

def index(request):
    if request.user.is_authenticated:
        return render(request, 'emploeeTreeTable.html')
    else:
        return redirect('auth/login')

def getjsonTable(request):
    if request.user.is_authenticated:

        response_data = list()

        employees = EmployeeTreeModel.objects.all().filter(level__lte=4).order_by('fullName')
        #response_data = serializers.serialize('json', employees)


        for i in employees:
            if i.level < 5:
                response_data +=[{
                    'position' : i.position,
                    'fullName': i.fullName,
                    'salary':i.salary,
                    'bossID':i.bossID,
                    'employeeDate': i.employeeDate,
                    'id': i.id,
                    'level':i.level,
                    'bossName':i.bossName
                }]




        return JsonResponse({'table':response_data}, safe=True)
    else:
        return redirect('auth/login')

def getTableByBossId(request):
    if request.user.is_authenticated:

        bossID = request.GET.get('bossID')
        order_by = request.GET.get('order_by') if request.GET.get('order_by') != '' else 'fullName'

        response_data = list()

        employees = EmployeeTreeModel.objects.all().filter(bossID=bossID).order_by(order_by)

        for i in employees:
            response_data += [{
                'position' : i.position,
                'fullName': i.fullName,
                'salary':i.salary,
                'bossID':i.bossID,
                'employeeDate': i.employeeDate,
                'id': i.id,
                'level':i.level,
                'bossName':i.bossName
            }]

        return JsonResponse({'table':response_data}, safe=True)
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
        ...
    else:
        # Return an 'invalid login' error message.
        pass

def serchby(request):
    if request.user.is_authenticated:
        QueryDict = request.GET.dict()
        response_data = list()
        key = ''
        val = ''
        for i in QueryDict:
            key = i
            val = QueryDict[i]

        if key=='position':
            employees = EmployeeTreeModel.objects.all().filter(position__icontains=val)
        elif key=='fullName':
            employees = EmployeeTreeModel.objects.all().filter(fullName__icontains=val)
        elif key=='salary_less':
            employees = EmployeeTreeModel.objects.all().filter(salary__lte=val)
        elif key=='salary_more':
            employees = EmployeeTreeModel.objects.all().filter(salary__gte=val)
        elif key=='employed_after':
            employees = EmployeeTreeModel.objects.all().filter(employeeDate__gte=val)
        elif key=='employed_before':
            employees = EmployeeTreeModel.objects.all().filter(employeeDate__lte=val)
        elif key=='bossID':
            employees = EmployeeTreeModel.objects.all().filter(bossID=val)


        for i in employees:
            response_data += [{
                'position' : i.position,
                'fullName': i.fullName,
                'salary':i.salary,
                'bossID':i.bossID,
                'employeeDate': i.employeeDate,
                'id': i.id,
                'level':i.level,
                'bossName':i.bossName
            }]

        return JsonResponse({'table':response_data}, safe=True)
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

