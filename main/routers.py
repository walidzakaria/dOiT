from rest_framework import routers
from .views import UserViewSet, ActivityTypeViewSet


router = routers.DefaultRouter()
#router.register(r'users', UserViewSet)
router.register(r'users-aaa', ActivityTypeViewSet)
