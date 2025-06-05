from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import Task


def _send_task_mail(subject: str, message: str, recipient: str) -> None:
    """Helper to send notification emails."""
    send_mail(
        subject,
        message,
        getattr(settings, "DEFAULT_FROM_EMAIL", "webmaster@localhost"),
        [recipient],
        fail_silently=True,
    )


@receiver(pre_save, sender=Task)
def task_status_change(sender, instance: Task, **kwargs):
    """Notify owner when task status is updated."""
    if not instance.pk:
        return
    try:
        previous = Task.objects.get(pk=instance.pk)
    except Task.DoesNotExist:
        return
    if previous.status != instance.status:
        subject = f"Task '{instance.title}' status changed"
        message = f"Status changed from '{previous.status}' to '{instance.status}'"
        _send_task_mail(subject, message, instance.owner.email)


@receiver(post_delete, sender=Task)
def task_deleted(sender, instance: Task, **kwargs):
    """Notify owner when task is deleted."""
    subject = f"Task '{instance.title}' closed"
    message = "The task has been closed and removed."
    _send_task_mail(subject, message, instance.owner.email)