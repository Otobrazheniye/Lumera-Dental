from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import( 
    User, 
    Organization, Membership,
)



# User



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