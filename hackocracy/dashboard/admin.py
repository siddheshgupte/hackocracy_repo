from django.contrib import admin

from .models import Profile, Exchanges

# Register your models here.
admin.site.register(Exchanges)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'political_party', 'party_image']

admin.site.register(Profile, ProfileAdmin)
