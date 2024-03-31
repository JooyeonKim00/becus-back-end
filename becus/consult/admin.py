from django.contrib import admin
from .models import Pconsult, Gconsult

# Register your models here.
admin.site.register(Pconsult)
admin.site.register(Gconsult)