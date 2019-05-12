from rest_framework import routers
from .views import RegionViewSet, CityViewSet


router = routers.DefaultRouter()

router.register(r'region', RegionViewSet)
router.register(r'city', CityViewSet)

urlpatterns = router.urls