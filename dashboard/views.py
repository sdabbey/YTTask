from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from accounts.models import Profile, User
from dashboard.models import Notification
from accounts.forms import ProfileForm
# Create your views here.

from django.db.models import Sum

@login_required(login_url="accounts:login_yttasker")
def dashboard(request):
    # Use prefetch_related with values() to fetch specific fields
    yttasker_tasks = YTTasker_task.objects.prefetch_related('task__point').filter(tasker=request.user).values('task__point')
    print(yttasker_tasks)
    # Calculate the point_sum directly from the queryset
    point_sum = sum(task['task__point'] for task in yttasker_tasks)

    # Fetch all tasks for the for loop
    tasks = Task.objects.all()

    return render(request, "dashboard/dashboard.html", {"tasks": tasks, "yttasker_tasks": yttasker_tasks, "point_sum": point_sum})

# @login_required(login_url="accounts:login_yttasker")
# def dashboard(request):
#     tasks = Task.objects.all()
#     yttasker_task = YTTasker_task.objects.all()

#     new_yttasker_task = YTTasker_task.objects.filter(tasker=request.user, completed=True)
#     point_sum = 0
#     for task in new_yttasker_task:
#         point_sum += task.task.point
    
#     return render(request, "dashboard/dashboard.html", {"tasks": tasks, "yttasker_tasks": yttasker_task, "point_sum": point_sum})

@login_required(login_url="accounts:login_yttasker")
def notification(request):
    new_yttasker_task = YTTasker_task.objects.filter(tasker=request.user, completed=True)
    point_sum = 0
    for task in new_yttasker_task:
        point_sum += task.task.point
    notifications = Notification.objects.all()
    faqs = FAQ.objects.all()
    return render(request, "dashboard/notification.html", {"notifications": notifications, "faqs": faqs, "point_sum": point_sum})

@login_required(login_url="accounts:login_yttasker")
def user_profile(request):
    if request.user.is_staff:

        return render(request, "dashboard/user_profile.html")
    new_yttasker_task = YTTasker_task.objects.filter(tasker=request.user, completed=True)
    point_sum = 0
    for task in new_yttasker_task:
        point_sum += task.task.point
    profile = Profile.objects.get(yttasker__email=request.user)
    return render(request, "dashboard/user_profile.html", {"yttasker_profile": profile,"point_sum": point_sum})
@login_required(login_url="accounts:login_yttasker")
def check_complete(request, task_title, id):
    yttasker_task = YTTasker_task.objects.filter(task=id, tasker=request.user).first()
    if request.method == "POST":
        code = request.POST.get("check_number")
        if code == yttasker_task.task.secret_code:
            yttasker_task.completed = True
            yttasker_task.save()
     
    
    return redirect("dashboard:dashboard")

def update_profile(request, id):
    form = ProfileForm()
    if request.method == 'POST':
        profile = Profile.objects.get(yttasker__email=request.user)
       
        profile.username = request.POST.get("username")

        profile.email = request.POST.get('email')
        profile.momo_number = request.POST.get("momo_number")
        profile.password = request.POST.get("password")
        profile.phonenumber = request.POST.get("phonenumber")
        profile.save()
        return redirect("dashboard:user_profile")
    return render(request, "dashboard/user_profile.html", {"form": form})
