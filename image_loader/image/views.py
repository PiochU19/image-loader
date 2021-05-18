from image_loader.image.models import MainImage, Image
from image_loader.image.serializers import ImageMainSerializer, GenerateLinkSerializer
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from image_loader.permissions import IsImageOwner, HasAbilityToGenerateExpiringLinks
from image_loader.image.utils import create_link
from django.views import View
from django.http import HttpResponse
from django.core import signing
from datetime import datetime
from django.utils import timezone


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


class GenerateLinkAPIView(APIView):
    """
    Endpoint which takes image name, seconds and size
    of an image as a data and returns temporary link
    """

    permission_classes = (HasAbilityToGenerateExpiringLinks,)
    serializer_class = GenerateLinkSerializer

    def post(self, request):
        data = request.data
        serializer = GenerateLinkSerializer(data=data, context={"request": request})

        if serializer.is_valid():

            link = create_link(data["expires_after"], data["image_name"], data["size"])

            return Response({"link": link}, status=status.HTTP_200_OK)
        return Response(serializer.errors)


class DynamicImageView(View):
    """
    View takes token as a argument
    and checkingif token does not expiried,
    then opens image and returns it
    """

    def get(self, request, token):
        values = signing.loads(token)
        expiry_date = datetime.fromisoformat(values[0])
        if expiry_date >= timezone.now():
            image_name = MainImage.objects.get(image_name=values[1])
            img = Image.objects.get(image_name=image_name, size=int(values[2])).image
            try:
                with open(f"media/{img.name}", "rb") as image:
                    return HttpResponse(image.read(), content_type="image/jpeg")
            except IOError:
                return HttpResponse("Something went wrong")
        return HttpResponse("Token expired")