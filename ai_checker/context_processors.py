from .models import Notification

def notification_count(request):
    """Add notification count to template context"""
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(
            recipient=request.user, 
            is_read=False
        ).count()
        return {'unread_notification_count': unread_count}
    return {'unread_notification_count': 0}