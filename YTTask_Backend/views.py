from django.shortcuts import render, redirect
from accounts.models import User
def home(request):
    return render(request, "landingpage.html")


def create_superuser(request):
    password = "testing321"
    if User.objects.filter(email='admin@yttask.com').exists():
        return redirect("landingpage")
    User.objects.create_superuser(email='admin@yttask.com', password=password)
    user = User.objects.get(email='admin@yttask.com')
    user.set_password(password)
    user.save()
    return redirect("landingpage")
