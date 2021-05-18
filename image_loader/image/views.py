from image_loader.image.models import MainImage
from image_loader.image.serializers import ImageMainSerializer
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from image_loader.permissions import IsImageOwner


class ImageMainViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    ViewSet with create, retrieve and list methods
    """

    permission_classes = (IsImageOwner,)
    serializer_class = ImageMainSerializer
    queryset = MainImage.objects.all()
    lookup_field = "image_name"

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return MainImage.objects.filter(user=self.request.user)