from django.contrib import admin

# Register your models here.
from .models import *

# These models are displayed on the admin page for the admin to modify/delete them.
admin.site.register(Email) 