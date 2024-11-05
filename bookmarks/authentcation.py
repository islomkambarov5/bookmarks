from django.contrib.auth.models import Users

class EmailAuthBackend:
    
    def authenticate(self, request, username=None, password=None):
        try:
            user = Users.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (Users.DoesNotExist, Users.MultipleObjectsReturned):
            return None
    
    def get_user(self, user_id):
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None