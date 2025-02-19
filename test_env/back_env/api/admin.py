from django.contrib import admin
from . import models

# Register your models here.
class CustomModelAdmin(admin.ModelAdmin):
    
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(CustomModelAdmin, self).__init__(model, admin_site)

class AdModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(AdModelAdmin, self).__init__(model, admin_site)

    readonly_fields=("summary",)

admin.site.register(models.Dealer, CustomModelAdmin)
admin.site.register(models.Ad, AdModelAdmin)
admin.site.register(models.Settings, CustomModelAdmin)

