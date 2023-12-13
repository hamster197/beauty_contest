from django.core.exceptions import PermissionDenied

def leader_check(user,):
    if not user.groups.filter(name='Leader').exists():
        raise PermissionDenied

    return True
