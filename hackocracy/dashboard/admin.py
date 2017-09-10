from django.contrib import admin
from .models import Profile
from .models import Transactions

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'political_party', 'party_image']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Transactions)