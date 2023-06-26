from django.contrib import admin
from .models import User, Subjects, Enrollment, Role


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'status', 'role']
    list_filter = ['status', 'role']
    search_fields = ['username', 'first_name', 'last_name', 'email']


class SubjectsAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'program', 'bodovi', 'sem_redovni', 'sem_izvanredni', 'izborni', 'nositelj']
    list_filter = ['izborni']
    search_fields = ['name', 'code', 'program', 'nositelj__username']


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'status']
    list_filter = ['status']
    search_fields = ['student__username', 'subject__name']




admin.site.register(User, UserAdmin)
admin.site.register(Subjects, SubjectsAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Role)

