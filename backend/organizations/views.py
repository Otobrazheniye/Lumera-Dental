# Rest
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets, serializers, status, mixins
from rest_framework.decorators import action
# from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.exceptions import TokenError


from .models import (
    Organization, Membership,
) 
from .serializers import (
    OrganizationSerializer, MembershipSerializer,
)


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

