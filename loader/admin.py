from django.contrib import admin
from .models import PassPhrase, Pi_login, FakeKey
# Register your models here.


class YourModelAdmin(admin.ModelAdmin):
    readonly_fields = ('keys',)
    list_display = ('date', 'id',)
    # ordering = ('-unlock_date',)  # Order by date in descending order
    # list_filter = ('unlock_date','passphrase',)
    search_fields = ('keys',)

admin.site.register(PassPhrase, YourModelAdmin)


class YourModelAdminFake(admin.ModelAdmin):
    list_display = ('fake_keys', 'id',)

admin.site.register(FakeKey, YourModelAdminFake)