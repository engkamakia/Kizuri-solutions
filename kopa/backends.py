from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class IDNumberBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, id_number=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=email, id_number=id_number)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
