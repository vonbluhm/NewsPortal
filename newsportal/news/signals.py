from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import PostCategory
from django.conf import settings


def send_notifications(preview, pk, header, subscribers):
    html_content = render_to_string(
        'newpost.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=header,
        body='',
        from_email=settings.SERVER_EMAIL,
        to=subscribers
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def new_post_notify(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.categories.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += categories.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.header, subscribers)
