from django.contrib import admin
from .models import User, OTPCode

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = (
        'id',
        'phone',
        'email',
        'is_staff',
    )
    list_display_links = ['phone']
    search_fields = (
        'phone',
        'email',
    )
    fieldsets = (
        (
            'Основная информация',
            {
                'fields': (
                    'phone',
                    'password',
                )
            }
        ),

        (
            'Личная информация',
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                    'avatar'
                )
            }
        ),

        (
            'Права',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            }
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'phone',
                    'password1',
                    'password2',
                ),
            },
        ),
    )



admin.site.register(OTPCode)