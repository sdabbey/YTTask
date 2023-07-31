from django import forms
from .models import YTTasker,Profile

class YTTaskerForm(forms.ModelForm):
   
    class Meta: 
        model = YTTasker
        fields = ('email','password', 'confirm_password', 'momo_number')


class ProfileForm(forms.ModelForm):
    class Meta: 
        model = Profile
        fields = ('username', 'email', 'momo_number', 'password', 'phonenumber')