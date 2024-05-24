from .models import Roles
import uuid


def create_role_cron():
    unique_string = str(uuid.uuid4())
    Roles.objects.create(name=unique_string)
