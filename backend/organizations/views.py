# Rest
from django.contrib.auth import authenticate
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets, serializers, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


from .models import (
    User,
    Organization, Membership,
) 
from .serializers import (
    RegistrationUserSerializer, LoginUserSerializer,
    MeUserSerializer, LogoutSerializer,
    OrganizationSerializer, MembershipSerializer,
)


#User
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return RegistrationUserSerializer
        elif self.action == "login":
            return LoginUserSerializer
        elif self.action == "me":
            return MeUserSerializer
        elif self.action =="logout":
            return LogoutSerializer
        return MeUserSerializer
    
    def get_permissions(self):
        if self.action in ("create", "login"):
            return [AllowAny()]
    
        if self.action in ("me", "logout"):
            return [IsAuthenticated()]
    
        return [IsAdminUser()]
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Registration successful",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": MeUserSerializer(user,context={"request": request},).data,
        },
        status=status.HTTP_201_CREATED,
    )

    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        user = authenticate(
            request = request,
            email = email,
            password = password
        )

        if not user:
            raise serializers.ValidationError("Invalid email or password")
        
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "message": "Login successful",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": MeUserSerializer(user,context={"request": request},).data,
        },
        status=status.HTTP_200_OK,
    )

    @action(detail=False, methods=["get","patch"])
    def me(self, request):
        if request.method == "GET":
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
        
    @action(detail=False, methods=["post"])
    def logout(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data["refresh"]

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            raise serializers.ValidationError("Invalid or expired refresh token")
        return Response(
            {"message": "Logout successful"},
            status=status.HTTP_200_OK,
        )

# Main
class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def destroy(self, request, *args, **kwargs):
        organization = self.get_object()
        # queryset = Organization.objects.filter(is_active=True)
        organization.is_active = False
        organization.save(update_fields=["is_active", "updated_at"])

        return Response(status=status.HTTP_204_NO_CONTENT)


class MembershipViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, 
    mixins.CreateModelMixin, mixins.DestroyModelMixin, 
    viewsets.GenericViewSet, mixins.UpdateModelMixin,):

    queryset = Membership.objects.select_related("clinic", "user")
    serializer_class = MembershipSerializer

