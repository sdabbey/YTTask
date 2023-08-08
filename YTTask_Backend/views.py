from django.shortcuts import render, redirect
from accounts.models import User
from dashboard.models import Task
def home(request):
    return render(request, "landingpage.html")

def sitemap(request):
    return render(request, "sitemap.xml")

def delete_tasks(request):
    tasks = Task.objects.all()
    tasks.delete()
    return redirect("landingpage")

def create_superuser(request):
    password = "testing321"
    if User.objects.filter(email='admin@yttask.com').exists():
        return redirect("landingpage")
    User.objects.create_superuser(email='admin@yttask.com', password=password)
    user = User.objects.get(email='admin@yttask.com')
    user.set_password(password)
    user.save()
    return redirect("landingpage")
