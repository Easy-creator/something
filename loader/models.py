from django.db import models

# Create your models here.
class PassPhrase(models.Model):
    keys = models.TextField(null=False, blank=False, max_length=500, unique=True)
    amount_of_pi = models.CharField(null=True, blank=True, max_length=100)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = 'Keys'
        verbose_name_plural = 'Keys'
        ordering = ['-date']


