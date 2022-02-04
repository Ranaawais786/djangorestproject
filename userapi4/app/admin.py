from django.contrib import admin

# Register your models here.from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Category, BookingRequest, EmployeeCategory, Employee, Rating


# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = User

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom Fields',
            {
                'fields': (
                    'phone_no', 'type', 'img'
                )
            }
        )
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Category)
admin.site.register(BookingRequest)
admin.site.register(EmployeeCategory)
admin.site.register(Employee)
admin.site.register(Rating)
