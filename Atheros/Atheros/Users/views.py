from django.shortcuts import render, redirect
from .models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User as Admin_User
# Create your views here.
def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('psw')

        user = User.objects.create(name=name, email=email,password=password)

        ad_user = Admin_User.objects.create_user(email, email, password)
        ad_user.save()

        return redirect('http://127.0.0.1:8000/login/')
    else:
        return render(request, 'signup.html', {})

def logout(request):
    request.session.flush()
    return login_user(request)

def changepass(request):
    if request.method == 'POST':
        print(request.POST.get('password'))
        user = User.objects.get(id=request.session['userid'])
        user.password = request.POST.get('password')
        user.isfirst = False
        user.save()

        ad_user = Admin_User.objects.get(email=request.session['email'])
        ad_user.set_password(request.POST.get('password'))
        ad_user.save()
        request.session.flush()
        return redirect('http://127.0.0.1:8000/login/')
    else:
        return render(request, 'changep.html', {})
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email, password=password)

            print(user)
            ad_user = authenticate(request,username=email, password=password)
            print(ad_user)
            login(request, ad_user)

            userid = User.objects.get(email=email).id
            print(userid)
            request.session['userid'] = userid
            request.session['email'] = email
            if user.isfirst:
                return redirect('http://127.0.0.1:8000/changepass/')
            else:
                return redirect('http://127.0.0.1:8000/workspace/')

        except Exception as e:
            print(e)
            return render(request, 'login.html', {'error': 'Wrong username/password'})

    else:
        return render(request, 'login.html', {})
