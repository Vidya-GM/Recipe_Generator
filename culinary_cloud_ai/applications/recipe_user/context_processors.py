from .models import Notification

def notification_count(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(notif_recipient=request.user, is_read=False).count()
        print(count)
        return {'unread_notif_count': count}
    print("User not authenticated!!")
    return {}