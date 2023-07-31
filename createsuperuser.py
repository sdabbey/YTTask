# custom_script.py

from django.core.management import call_command

def create_superuser():
    call_command('createsuperuser', '--noinput', username='admin', email='admin@yttask.com')
