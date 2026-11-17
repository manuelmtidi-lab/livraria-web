from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Cliente


@receiver(post_save, sender=User)
def criar_cliente(sender, instance, created, **kwargs):
    if created:
        Cliente.objects.get_or_create(
            usuario=instance,
            defaults={'nome': instance.get_full_name() or instance.username},
        )
