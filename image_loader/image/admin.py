from django.contrib import admin
from image_loader.image.models import Image, MainImage


admin.site.register(Image)
admin.site.register(MainImage)