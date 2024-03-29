from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from accounts.models import Profile, User, YTTasker_payout
from dashboard.models import Notification
from accounts.forms import ProfileForm
from django.core.paginator import Paginator



from YTTask_Backend.views import tasks

@login_required(login_url="accounts:login_yttasker")
def dashboard(request):
    # Fetch all tasks


    # Use only() to fetch specific fields from YTTasker_task and Task
    yttasker_tasks = YTTasker_task.objects.filter(tasker=request.user)

    # point_sum=0
    # for yttasker_task in yttasker_tasks:
    #     if yttasker_task.completed is True:
    #         task_points = task_points + yttasker_task.task.point
    #task_points = YTTasker_task.objects.filter(tasker=request.user, completed=True).values_list('task__point', flat=True)
    task_points = yttasker_tasks.filter(completed=True).values_list('task__point', flat=True)

    # Calculate the point_sum directly from the flat list
    point_sum = sum(point for point in task_points if point is not None)
    # yttasker_payout, created = YTTasker_payout.objects.get_or_create(tasker=request.user)
    # yttasker_payout.payout = point_sum
    # yttasker_payout.save()


    yttasker_payout = YTTasker_payout.objects.filter(tasker__email=request.user).exists()
    if yttasker_payout is False:
        YTTasker_payout.objects.create(tasker=request.user, payout=point_sum)
    else:
        yttasker_payout_old = YTTasker_payout.objects.get(tasker=request.user)
        point_sum = yttasker_payout_old.payout + point_sum
        yttasker_payout_old.payout = point_sum
        
    # Paginate the tasks
    paginator = Paginator(tasks, 10)  # Show 10 tasks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "dashboard/dashboard.html", {
        "page_obj": page_obj,
        "yttasker_tasks": yttasker_tasks,
        "point_sum": YTTasker_payout.objects.get(tasker__email=request.user).payout
    })





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
    return render(request, "dashboard/notification.html", {"notifications": notifications, "faqs": faqs, "point_sum": YTTasker_payout.objects.get(tasker__email=request.user).payout})

@login_required(login_url="accounts:login_yttasker")
def user_profile(request):
    if request.user.is_staff:

        return render(request, "dashboard/user_profile.html")
    new_yttasker_task = YTTasker_task.objects.filter(tasker=request.user, completed=True)
    point_sum = 0
    for task in new_yttasker_task:
        point_sum += task.task.point
    profile = Profile.objects.get(yttasker__email=request.user)
    return render(request, "dashboard/user_profile.html", {"yttasker_profile": profile,"point_sum": YTTasker_payout.objects.get(tasker__email=request.user).payout})

@login_required(login_url="accounts:login_yttasker")
def check_complete(request, id):
    yttasker_task = YTTasker_task.objects.get(task=id, tasker=request.user)
    print(yttasker_task)
    if request.method == "POST":
        code = request.POST.get("check_number")
        if code == yttasker_task.task.secret_code:
            yttasker_task.completed = True
            yttasker_task.save()

            yttasker_payout = YTTasker_payout.objects.get(tasker__email=request.user)
            print(yttasker_payout)
            yttasker_payout.payout = yttasker_payout.payout + yttasker_task.task.point
            yttasker_payout.save()
    
    # Get the current URL from request.META
    current_url = request.META['HTTP_REFERER']
    
    # Redirect back to the current page
    return redirect(current_url)



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
