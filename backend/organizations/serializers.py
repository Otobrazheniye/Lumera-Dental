from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Organization, Membership
        ) 


#User
User = get_user_model()


class RegistrationUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6, style={"input_type": "password"},)
    
    class Meta: 
        model = User
        fields = (
            "id", "email", 
            "password", "first_name",
            "last_name", "phone",
            "date_joined", "updated_at",
        )

        read_only_fields = (    
            "id",
            "date_joined", "updated_at",
            )

    def validate_email(self, value):
        return value.lower().strip()

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password =  serializers.CharField(write_only=True, min_length=6)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        # Улучшить через login flow.

        return attrs


class MeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id", "email", 
            "first_name", "last_name", 
            "phone", "date_joined", 
        )
        
        read_only_fields = ("id", "date_joined")


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


# Main
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
