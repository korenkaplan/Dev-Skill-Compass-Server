from core.models import RoleListingsCount


def format_role_listings(role_listings: list[RoleListingsCount]):
    return [{'id': item.id, 'role_id': item.role_id.id, 'counter': item.counter} for item in role_listings]


def get_count_object_by_role_id(role_id: int):
    obj = RoleListingsCount.objects.filter(role_id=role_id).first()
    if obj:
        return format_role_listings([obj])
    return None
