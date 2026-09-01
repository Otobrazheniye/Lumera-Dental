from rest_framework import serializers
from .models import (
    Organization, Membership
        ) 


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = (
            "id", "name",
            "slug", "is_active",
            "created_at", "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at", "updated_at",
        )


        def validate_name(self, value):
            value = value.strip()

            if not value:
                raise serializers.ValidationError(
                    "Organization name cannot be empty."
                )

            return value

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = (
            "id",
            "clinic", "user",
            "role", "created_at",
        )
        read_only_fields = ("id", "created_at")

    def validate_clinic(self, value):
        if not value.is_active:
            raise serializers.ValidationError(
                "Cannot add a member to an inactive clinic."
            )
        return value


    def validate(self, attrs):
        clinic = attrs.get("clinic", self.instance.clinic if self.instance else None)
        user = attrs.get("user", self.instance.user if self.instance else None)

        memberships = Membership.objects.filter(
            clinic=clinic, user=user,
        )

        if self.instance:
            memberships = memberships.exclude(
            pk=self.instance.pk
        )

        if memberships.exists():
            raise serializers.ValidationError("This user is already a member of this clinic.")

        return attrs
