from rest_framework import serializers
from image_loader.image.models import Image, MainImage
from image_loader.plan.models import Plan, UserPlan
from django.core.files.images import get_image_dimensions
from image_loader.image.utils import get_resized_image
from django.core.exceptions import ObjectDoesNotExist


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

    images = ImageSerializer(many=True, read_only=True)
    image = serializers.ImageField(write_only=True, required=True)

    class Meta:
        model = MainImage
        fields = ("image_name", "images", "image")
        extra_kwargs = {"image_name": {"read_only": True}}
        lookup_field = "image_name"

    def create(self, validated_data):
        """
        Create method
        """
        plan = UserPlan.objects.get(user=validated_data["user"]).plan
        image = validated_data["image"]
        main_image = MainImage.objects.create(
            user=validated_data["user"], image_name=str(image).split(".")[0]
        )

        if plan.acces_to_the_og:
            Image.objects.create(
                image_name=main_image, size=get_image_dimensions(image)[1], image=image
            )
        for size in plan.get_allowed_sizes():
            in_memory_uploaded_file = get_resized_image(image, int(size))
            print(in_memory_uploaded_file)
            Image.objects.create(
                image_name=main_image, size=size, image=in_memory_uploaded_file
            )
        return main_image

    def validate(self, data):
        """
        Place where data is validated
        """
        if (len(str(data["image"]).split(".")) > 3) or (
            str(data["image"]).split(".")[1].lower() not in ["jpg", "png", "jpeg"]
        ):
            raise serializers.ValidationError({"image": "Incorrect file!"})
        if (
            MainImage.objects.filter(
                image_name=str(data["image"]).split(".")[0]
            ).count()
            > 0
        ):
            raise serializers.ValidationError(
                {"image": "Image with this name already exists"}
            )
        return data


class GenerateLinkSerializer(serializers.Serializer):
    """
    Serializer for GenerateLinkAPIView
    """

    expires_after = serializers.IntegerField(required=True, write_only=True)
    image_name = serializers.CharField(max_length=50, write_only=True, required=True)
    size = serializers.IntegerField(required=True, write_only=True)
    link = serializers.URLField(read_only=True)

    class Meta:
        fields = ("expires_after", "image_name", "size", "link")

    def validate(self, data):
        """
        method where data is validated
        """
        user = self.context["request"].user

        if data["expires_after"] > 30000 or data["expires_after"] < 300:
            raise serializers.ValidationError(
                {"expires_after": "expires_after must be between 300 and 30000"}
            )
        if data["size"] > 3000 or data["size"] < 200:
            raise serializers.ValidationError(
                {"size": "size must be between 200 and 3000"}
            )
        try:
            main_image = MainImage.objects.get(user=user)
            image = Image.objects.get(image_name=main_image, size=data["size"])
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"error": "Something went wrong"})
        return data