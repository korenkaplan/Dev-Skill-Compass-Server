from core.models import Roles


def create_role(name: str):
    return Roles.objects.create(name=name)


def get_role_by_name(name: str) -> Roles:
    return Roles.objects.get(name=name)


def get_role_by_pk(id_to_find: int) -> Roles:
    return Roles.objects.get(id=id_to_find)
