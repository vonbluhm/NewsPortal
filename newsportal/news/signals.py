from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import PostCategory
from .tasks import send_notifications


@receiver(m2m_changed, sender=PostCategory)
def new_post_notify(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add' and instance.__class__.__name__ == 'Post':
        categories = instance.categories.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += categories.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notifications.apply_async(instance.preview(), instance.pk, instance.header, subscribers)
