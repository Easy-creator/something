from django.contrib import admin
from .models import PassPhrase, Pi_login
# Register your models here.


class YourModelAdmin(admin.ModelAdmin):
    list_display = ('date', 'id',)
    # ordering = ('-unlock_date',)  # Order by date in descending order
    # list_filter = ('unlock_date','passphrase',)
    # search_fields = ('passphrase', 'unlock_date', 'amount')

admin.site.register(PassPhrase, YourModelAdmin)