from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator


class MainImage(models.Model):
    """
    Parent table for Image
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_image")
    image_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.image_name


class Image(models.Model):
    """
    One Image for One size
    """

    image_name = models.ForeignKey(MainImage, on_delete=models.CASCADE, related_name='images')
    size = models.IntegerField(
        validators=[MaxLengthValidator(3000), MinLengthValidator(200)]
    )
    image = models.ImageField(upload_to="images/")