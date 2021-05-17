from image_loader.image.views import ImageMainViewSet
from rest_framework.routers import DefaultRouter

app_name = "image"

router = DefaultRouter()
router.register(r"image", ImageMainViewSet)

urlpatterns = router.urls