from rest_framework import serializers

from images.models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Image
