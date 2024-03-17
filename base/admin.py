from django.contrib import admin
from .models import User, DoctorInfo, Specialization
from django.utils.translation import gettext as _


# Register your models here.


class DoctorInfoAdmin(admin.ModelAdmin):
    @staticmethod
    def make_doctor(modeladmin, request, queryset):
            for doctor_info in queryset:
                user = doctor_info.user
                user.isDoctor = True
                user.save()
    make_doctor.short_description = "Zatwierdź wybranych użytkowników"
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        actions['make_doctor'] = (self.make_doctor, 'make_doctor', _("Make selected users doctors"))
        actions['delete_selected'] = (self.delete_selected, 'delete_selected', _("Delete selected %(verbose_name_plural)s"))
        return actions

    def delete_selected(self, request, queryset):
        pass
    
admin.site.register(User)

admin.site.register(DoctorInfo, DoctorInfoAdmin)
admin.site.register(Specialization)