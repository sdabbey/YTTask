from django.urls import path
from . import views
app_name = "dashboard"
urlpatterns = [
   path('', views.dashboard, name="dashboard"),
   path('notification/', views.notification, name="notification"),
   path('user_profile/', views.user_profile, name="user_profile"),
   path('user_profile/update/<int:id>/', views.update_profile, name="update_profile"),
   path('check_complete/<str:task_title>/<int:id>/', views.check_complete, name="check_complete")
   
]
