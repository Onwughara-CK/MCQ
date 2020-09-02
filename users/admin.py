from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'teacher')
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, UserAdmin)
