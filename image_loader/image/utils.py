from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image as PillowImage


def get_resized_image(memory_uploaded_image, height):
    img = PillowImage.open(memory_uploaded_image)
    og_height, og_width = img.size
    proportions = height / og_height
    width = int(og_width * proportions)
    resized = img.resize((height, width))
    thumb_io = BytesIO()
    resized.save(thumb_io, format=img.format)

    return InMemoryUploadedFile(thumb_io, u"image", str(memory_uploaded_image), img.format, None, None)