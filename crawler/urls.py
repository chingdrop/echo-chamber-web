from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'results', views.ResultViewSet)

urlpatterns = router.urls