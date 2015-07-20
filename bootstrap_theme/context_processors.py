from django.conf import settings

def system_message(req):
    """
    This function is to display a system-wide message to connected users.
    An example would be stating when the server is going to have a maintaince period.
    """
    if hasattr(settings, 'SYSTEM_MESSAGE'):
        return {'SYSTEM_MESSAGE': settings.SYSTEM_MESSAGE}
    return {}
