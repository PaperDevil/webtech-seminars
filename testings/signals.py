from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Question


@receiver(post_save, sender=Question)
def my_handler(sender, **kwargs):
    print("Объект сохранён!")