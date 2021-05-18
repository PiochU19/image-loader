from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image as PillowImage
from django.core import signing
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from django.conf import settings


def get_resized_image(memory_uploaded_image, height):
    """
    Function returns resized InMemoryUploadedFile
    which can be saved to the db in the future
    """
    img = PillowImage.open(memory_uploaded_image)
    og_width, og_height = img.size
    proportions = height / og_height
    width = int(og_width * proportions)
    resized = img.resize((width, height), PillowImage.ANTIALIAS)
    thumb_io = BytesIO()
    resized.save(thumb_io, format=img.format)

    return InMemoryUploadedFile(thumb_io, u"image", str(memory_uploaded_image), img.format, None, None)


def create_link(seconds, image_name, size):
    """
    Function returns temporary link to the image
    """
    token = signing.dumps([str(timezone.now() + timedelta(seconds=int(seconds))), image_name, size])
    return settings.SERVER_PATH + reverse("image:dynamic-image", kwargs={"token": token})
