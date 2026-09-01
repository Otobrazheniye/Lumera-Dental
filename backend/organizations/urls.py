from rest_framework.routers import DefaultRouter

from .views import (
    OrganizationViewSet, MembershipViewSet,
)


router = DefaultRouter()
router.register("organizations", OrganizationViewSet, basename="organization")
router.register("memberships", MembershipViewSet, basename="membership")


urlpatterns = router.urls
