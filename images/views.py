from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from images.models import Image
from images.serializers import ImageSerializer


class ImageViewSet(ModelViewSet):
    serializer_class = ImageSerializer

    def get_queryset(self):
        user = self.request.user
        return Image.objects.filter(author=user)
