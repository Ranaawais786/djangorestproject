from django.contrib import admin
from .models import User, Smile,DailyQuote,Goal,Activity,Favourite,Community,Smilescience,Resource
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom Fields',
            {
                'fields': (
                    'GENDER', 'AGE', 'RELATIONSHIP', 'CHILDREN', 'GOAL','NAME'
                )
            }
        )
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(DailyQuote)
admin.site.register(Smile)
admin.site.register(Goal)
admin.site.register(Activity)
admin.site.register(Favourite)
admin.site.register(Community)
admin.site.register(Smilescience)
admin.site.register(Resource)