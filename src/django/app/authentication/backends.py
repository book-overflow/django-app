from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError

UserModel = get_user_model()

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        
        if not user.is_active:
            raise ValidationError("Account is inactive. Please click the account activation link in your email.")
        
        # password check handled by ModelBackend