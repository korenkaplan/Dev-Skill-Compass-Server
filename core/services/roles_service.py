import os
import django
from core.models import Roles


# Initialize Django
django.setup()


def create_role(name: str):
    return Roles.objects.create(name=name)


def get_role_by_name(name: str) -> Roles:
    return Roles.objects.get(name=name)


def get_role_by_pk(id_to_find: int) -> Roles:
    return Roles.objects.get(id=id_to_find)


def get_roles(names: list[str]) -> list[Roles]:
    pass


def update_role(pk: int, name: str) -> Roles:
    pass


def delete_role(pk: int) -> Roles:
    pass


role = create_role("backend_developer")
print(role)
