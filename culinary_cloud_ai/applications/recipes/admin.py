from django.contrib import admin
from applications.recipe_user.models import RecipeUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = RecipeUser

    list_display = ('username', 'email', 'last_login', 'profile_image')

    readonly_fields = ('created_at', 'updated_at')

    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields", {'fields': ('date_of_birth', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'bio', 'profile_image', 'password1', 'password2'),
        }),
    )


admin.site.register(RecipeUser, CustomUserAdmin)