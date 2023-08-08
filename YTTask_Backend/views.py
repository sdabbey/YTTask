from django.shortcuts import render, redirect, HttpResponse
from accounts.models import User
from dashboard.models import Task
import json
from django.db import transaction
def home(request):
    return render(request, "landingpage.html")

def sitemap(request):
    return render(request, "sitemap.xml")

def create_tasks(request):
    # Read data from the JSON file
    file_path = "templates/tasks.json"
    with open(file_path) as json_file:
        tasks_data = json.load(json_file)

    # Loop through the tasks data and create Task objects
    if request.user.is_superuser:
        with transaction.atomic():
            task_objects = [
                Task(prompt=prompt, secret_code=secret_code, point=0.02)
                for prompt, secret_code in tasks_data.items()
            ]
            Task.objects.bulk_create(task_objects)

    return HttpResponse("Access denied")

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
