from django.shortcuts import render, HttpResponse
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import UserRegistrationModel, EmployeeEmotionsModel
from datetime import datetime


# Create your views here.
def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()
            return render(request, 'UserRegistrations.html', {'form': form})
        else:
            messages.success(request, 'Email or Mobile Already Existed')
            print("Invalid form")
    else:
        form = UserRegistrationForm()
    return render(request, 'UserRegistrations.html', {'form': form})


def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                print("User id At", check.id, status)
                return render(request, 'users/UserHome.html', {})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'UserLogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'UserLogin.html', {})


def UserHome(request):
    return render(request, 'users/UserHome.html', {})


def StartEmotions(request):
    from .utility.findemotions import StartEmloyeeEmotions
    obj = StartEmloyeeEmotions()
    result_list = obj.start_process()
    if result_list:
        from collections import Counter
        sort = Counter(result_list)
        emotions_counts = sort.most_common(7)
        filters_emo = emotions_counts[0]
        emotion = filters_emo[0]
        count = filters_emo[1]
        print(f'Emotions {emotion} and its count {count}')
        user_name = request.session['loggeduser']
        login_id = request.session['loginid']
        email = request.session['email']
        c_date = datetime.now()
        EmployeeEmotionsModel.objects.create(user_name=user_name, login_id=login_id, email=email, emotion=emotion,
                                             count=count, c_date=c_date)

    return render(request, 'users/UserHome.html', {})

def EmployeeEmotionHistory(request):
    login_id = request.session['loginid']
    data  = EmployeeEmotionsModel.objects.filter(login_id=login_id)
    return render(request, 'users/EmployeeEmotions.html', {'data':data})


def Training(request):
    from .utility.StartTraining import InitializeTraining
    obj = InitializeTraining()
    obj.start_process()
    return render(request, 'users/UserHome.html', {})