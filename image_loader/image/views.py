from image_loader.image.models import MainImage
from image_loader.image.serializers import ImageMainSerializer
from rest_framework import viewsets, mixins
from rest_framework.response import Response


class ImageMainViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    ViewSet with create, retrieve and list methods
    """

    serializer_class = ImageMainSerializer
    queryset = MainImage.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)