# custom_script.py

from django.core.management import call_command


import os
from django.core.management import call_command
from accounts.models import User
def create_superuser():
    password = os.environ.get('SUPERUSER_PASSWORD', 'default_password')
    call_command('createsuperuser', '--noinput', email='admin@yttask.com')
    user = User.objects.get(email='admin@yttask.com')
    user.set_password(password)
    user.save()
