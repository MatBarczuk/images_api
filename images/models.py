from django.contrib.auth import get_user_model
from django.db import models

from helpers.image_resizing import ThumbnailMakerService
from images.validators import validate_file_type


class Image(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='images')
    url = models.FileField(upload_to='images/', validators=[validate_file_type])
    name = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        tn_maker = ThumbnailMakerService()
        tn_maker.make_thumbnails([self.url.name])

    def __str__(self):
        return self.name
