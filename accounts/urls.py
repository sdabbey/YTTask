from django.urls import path
from .views import create_yttasker, login_yttasker, logout_yttasker
app_name = "accounts"
urlpatterns = [
   path('create_yttasker/', create_yttasker, name="create_yttasker"),
   path('login_yttasker/', login_yttasker, name="login_yttasker"),
   path('logout_yttasker/', logout_yttasker, name="logout_yttasker")

]
