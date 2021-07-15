from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Department)
admin.site.register(User)
admin.site.register(Equipment)
admin.site.register(MaintenanceTicket)
admin.site.register(UserRequest)
admin.site.register(Team)
