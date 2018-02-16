from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate , logout
from django.shortcuts import render, redirect
from django.http import *
from accounts.forms import SignUpForm,LoginForm



@login_required
def home(request):
    return render(request, 'home.html')

def login_view(request):
    
    if request.user.is_authenticated():
        return redirect('home')
        
    username = password = ''
    context = {
        'form':LoginForm(),
        'title':'RoomMate'
    }
    
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                context.update({'warning':'Your acoount is Inactive'})
                return render(request,'roommate/login.html',context) 
        else:
            context.update({'error':'Invalid Username Or Password..'})
            return render(request,'roommate/login.html',context)        

    return render(request,'roommate/login.html',context)


def register(request):
    
    if request.user.is_authenticated():
        return redirect('home')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'roommate/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')