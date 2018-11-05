from django.contrib import admin
from .models import workspace
from .models import Channel
# Register your models here.

admin.site.register(workspace)
admin.site.register(Channel)
