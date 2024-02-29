import logging
import random

from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.template.defaultfilters import slugify

from core_auth.models.user import CustomUser
from core_management.models import Links
from entities.investor.models.models import Investor
from entities.startup.models.models import Startup


logger = logging.getLogger(__name__)

not_testing_env = settings.TESTING_ENV is False


# When we need to save files using the instance id we need to create it first without any files
# and then perform an update otherwise id would be None
# skip_saving_files_before_save saves files to a temporary variable
# save_files_after_save updates the instance with the files once we had an id
@receiver(models.signals.pre_save)
def skip_saving_files_before_save(sender, instance, **kwargs):
    # Exit if instance already has id or doesn't have id attribute
    if not hasattr(instance, "id") or instance.id:
        return
    # Set a temporary attribute to save files
    setattr(instance, "_unsaved_files", {})
    # Iterate all ImageFields and FileFields in model
    for field in sender._meta.fields:
        if (
            field.__class__.__name__ == "ImageField"
            or field.__class__.__name__ == "FileField"
        ):
            # Save field value to _unsaved_files dict and set it to none so it does not get saved with id=None
            field_name = field.name
            field_value = getattr(instance, field.name)
            if field_value:
                instance._unsaved_files[field_name] = field_value
                setattr(instance, field_name, None)


@receiver(models.signals.post_save)
def save_files_after_save(sender, instance, created=False, **kwargs):
    if created and hasattr(instance, "_unsaved_files"):
        for key, value in instance._unsaved_files.items():
            setattr(instance, key, value)
        instance.save(update_fields=instance._unsaved_files.keys())
        instance._unsaved_files = {}


@receiver(models.signals.pre_save, sender=CustomUser)
def generate_permaname_customuser(sender, instance, **kwargs):
    if instance.permaname:
        return
    try:
        clear_first_name = slugify(instance.first_name)
        clear_last_name = slugify(instance.last_name)
    except:
        return
    if not (clear_first_name and clear_last_name):
        return
    instance.permaname = "%s-%s" % (clear_first_name, clear_last_name)
    while sender.objects.filter(permaname=instance.permaname).exists():
        instance.permaname = "%s-%d" % (instance.permaname, random.randint(1, 9))
    if len(instance.permaname) > 50:
        instance.permaname = ""


# Create values automatically
@receiver(models.signals.pre_save, sender=Investor)
@receiver(models.signals.pre_save, sender=Startup)
def create_links(sender, instance, **kwargs):
    if not instance.links:
        instance.links = Links.objects.create()
