from django.contrib.auth.backends import BaseBackend
from .models import User  # Import your custom User model

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = User.objects.get(email=email)  # Retrieve the user based on the email
            if user.check_password(password):    # Check if the password matches
                return user  # Return the user object if authentication is successful
        except User.DoesNotExist:
            return None  # Return None if the user is not found or password doesn't match

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)  # Retrieve the user based on the primary key
        except User.DoesNotExist:
            return None  # Return None if the user is not found
