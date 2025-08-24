from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Comment, Post

@receiver(post_save, sender=Comment)
def notify_on_comment(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        subject = f"New comment on your post: {post.title}"
        body = f"{instance.user.username} commented:\n\n{instance.text}\n\n(Moderation status: {'Approved' if instance.is_approved else 'Pending'})"
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [post.author.email])

@receiver(post_save, sender=Post)
def alert_on_new_post(sender, instance, created, **kwargs):
    if created:
        subject = f"New blog post published: {instance.title}"
        body = f"{instance.author.username} published a new post.\n\n{instance.content[:200]}..."
        # For demo, email site admins (or change to a list)
        recipients = [u.email for u in instance.author.__class__.objects.filter(is_staff=True) if u.email]
        if recipients:
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipients)
