from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import( 
    User, 
    Organization, Membership,
)



# User
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        "email", "first_name",
        "last_name",
        "phone", "date_joined",
        "updated_at",
    ) 
    list_filter = (
        "is_active", "is_staff", 
        "is_superuser", "date_joined",
    )
    search_fields = (
        "email", "first_name",
        "last_name", "phone",
    )
    ordering = ("last_name", "-date_joined")

    fieldsets = (
        (None, { 
            "fields": ("email", "password")}),
        ("Personal info", {
            "fields": (
                "first_name",
                "last_name", "phone",
                )
        }),
        ("Permission", {
            "fields": ( 
                "is_active", "is_staff",
                "is_superuser", "groups",
                "user_permissions",)
        }),
        ("Important dates", {
            "fields": (
                "last_login", "date_joined",
                "updated_at",
                )
        })
    )
    readonly_fields = (
        "date_joined", "last_login",
        "updated_at",
        )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "first_name",
                "last_name", "phone",
                "password1", "password2",
                "is_staff", "is_active",
            ),
        }),
    )

# Main
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name",
        "slug", "is_active",
        "created_at", "updated_at",
    )

    search_fields = ("name", "slug",)
    list_filter = ("is_active",)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user",
        "clinic", "created_at",
        )

    search_fields = ("user__email", "clinic__name",)
    # → зайди по ForeignKey в user и ищи по его полю email.
    list_filter = ("clinic",)