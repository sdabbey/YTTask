from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import YTTaskerForm
from django.contrib.auth import authenticate, login, logout

from .models import YTTasker, User
# Create your views here.
def create_yttasker(request):
    if request.method == "POST":
        check1 = False
        check2 = False

        form = YTTaskerForm()
        email = request.POST.get("email")
        momo_number = request.POST.get("momo_number")
        password1 = request.POST.get("password")
        password2 = request.POST.get("confirm_password")
        if YTTasker.objects.filter(email=email).exists():
            check1 = True
            messages.error(request, 'Email already registered',
                           extra_tags='alert alert-warning alert-dismissible fade show')
           
            
        if password1 != password2:
            check2 = True
            messages.error(request, 'Passwords do not match',
                           extra_tags='alert alert-warning alert-dismissible fade show')
        
        if check1 or check2:
            messages.error(
                request, "Registration Failed", extra_tags='alert alert-warning alert-dismissible fade show')
            return redirect('accounts:create_yttasker')
        else:
           
            user = User.objects.create_user(email=email, password=password1)
            yttasker = YTTasker.objects.create(y_user=user, email=email, momo_number=momo_number, password=password1, confirm_password=password2)
            messages.success(
                request, f'Thanks for registering {yttasker.email}!',
                extra_tags='alert alert-success alert-dismissible fade show')
            return redirect("accounts:login_yttasker")
    else:
        form = YTTaskerForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_yttasker(request):
    email = ""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        yttasker = authenticate(request, email=email, password=password)
        print(yttasker)
        if yttasker is not None:
            login(request, yttasker)
            return redirect('dashboard:dashboard')
        else:
            messages.error(request, "Email Or Password is incorrect! Try again",
                               extra_tags='alert alert-warning alert-dismissible fade show')
    return render(request, "accounts/login.html", {"email":email})

def logout_yttasker(request):
    logout(request)
    return redirect('accounts:login_yttasker')