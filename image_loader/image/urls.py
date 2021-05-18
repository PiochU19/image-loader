from django.urls import path
from image_loader.image.views import (
    ImageMainViewSet,
    GenerateLinkAPIView,
    DynamicImageView,
)
from rest_framework.routers import DefaultRouter

app_name = "image"

urlpatterns = [
    path("image/link/", GenerateLinkAPIView.as_view(), name="generate-link"),
    path("tempimg/<str:token>/", DynamicImageView.as_view(), name="dynamic-image"),
]

router = DefaultRouter()
router.register(r"image", ImageMainViewSet)

urlpatterns += router.urls