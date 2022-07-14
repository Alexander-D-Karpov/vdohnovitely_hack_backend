from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from common.generators import generate_charset
from .models import User, Subscriber


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created:
        instance.username = instance.email
        instance.slug = generate_charset(20)
        instance.set_password(instance.password)
        instance.save()


@receiver(post_save, sender=Subscriber)
def create_user(sender, instance, created, **kwargs):
    if created:
        instance.author.subscriber_count += 1
        instance.author.save(update_fields=["subscriber_count"])
        instance.save()


@receiver(post_delete, sender=Subscriber)
def delete_user(sender, instance, **kwargs):
    instance.author.subscriber_count -= 1
    instance.author.save()
    instance.delete()
