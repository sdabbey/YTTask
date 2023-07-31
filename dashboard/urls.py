from django.urls import path
from .views import *
app_name = "dashboard"
urlpatterns = [
   path('', dashboard, name="dashboard"),
   path('notification/', notification, name="notification"),
   path('user_profile/', user_profile, name="user_profile"),
   path('user_profile/update/<int:id>/', update_profile, name="update_profile"),
   path('check_complete/<str:task_title>/<int:id>/', check_complete, name="check_complete")
   
]
