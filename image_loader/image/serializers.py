from rest_framework import serializers
from image_loader.image.models import Image, MainImage


class ImageSerializer(serializers.ModelSerializer):
    """
    Serializer returns Foreign Keys for MainImage Model
    """

    class Meta:
        model = Image
        fields = ("size", "image")


class ImageMainSerializer(serializers.ModelSerializer):
    """
    MainImage Model serializer
    """

    images = ImageSerializer(many=True)
    image = serializers.ImageField(write_only=True, required=True)

    class Meta:
        model = MainImage
        fields = ("image_name", "images", "image")
        extra_kwargs = {"image_name": {"read_only": True}}
        lookup_field = "image_name"