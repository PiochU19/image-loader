from image_loader.image.models import Image, MainImage
from image_loader.plan.models import Plan, UserPlan
from image_loader.image.serializers import ImageMainSerializer
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.files.images import get_image_dimensions


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

    def create(self, request):
        """
        Override create method (POST)
        """
        user = request.user
        plan = get_object_or_404(UserPlan, user=user).plan
        image = request.data["image"]
        main_image = MainImage.objects.create(user=user, image_name=str(image)[:-4])

        if plan.acces_to_the_og:
            Image.objects.create(
                image_name=main_image, size=get_image_dimensions(image)[1], image=image
            )
        return Response(serializer.data)