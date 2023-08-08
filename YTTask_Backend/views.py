from django.shortcuts import render, redirect, HttpResponse
from accounts.models import User
from dashboard.models import Task, YTTasker_task
import json
from django.db import transaction
def home(request):
    return render(request, "landingpage.html")

def sitemap(request):
    return render(request, "sitemap.xml")


users = User.objects.all()
def create_yttasker_tasks(tasks):

    
    for user in users:
        yttasker_tasks = [YTTasker_task(task=task, tasker=user) for task in tasks]
        YTTasker_task.objects.bulk_create(yttasker_tasks)

def create_tasks(request):
    # Read data from the JSON file
    file_path = "templates/tasks.json"
    with open(file_path) as json_file:
        tasks_data = json.load(json_file)

    # Loop through the tasks data and create Task objects
    if request.user.is_superuser:
        tasks_to_create = [
        Task(prompt=prompt, secret_code=secret_code, point=0.02)
        for prompt, secret_code in tasks_data.items()
        ]
        Task.objects.bulk_create(tasks_to_create)
        
        # Call the function to create corresponding YTTasker_task instances
        create_yttasker_tasks(tasks_to_create)
        
        return HttpResponse("Successfully created")

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
