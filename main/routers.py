from rest_framework import routers
from .viewsets import UserViewSet, ActivityTypeViewSet, ActivityViewSet, UserActivityViewSet, UserFullActivityViewSet, GetActivityListByUser

router = routers.DefaultRouter()
router.register(r'activity-type', ActivityTypeViewSet)
router.register(r'activity', ActivityViewSet)
router.register(r'user-activity', UserActivityViewSet)
router.register(r'user-full-activity', UserFullActivityViewSet)