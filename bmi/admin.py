from django.contrib import admin
from . models import Bmi
# Register your models here.
# admin.site.register(Bmi)


class BmiAdmin(admin.ModelAdmin):
    # specifying in tuple list of names we want to be displayed in the admin section
    list_display = ('user', 'weight', 'height', 'bmi', 'date')

admin.site.register(Bmi, BmiAdmin)