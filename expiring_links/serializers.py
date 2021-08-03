from rest_framework import serializers

from images.models import Image


class ExpiringLinkGeneratorSerializer(serializers.Serializer):
    url = serializers.URLField()
    expiration_time = serializers.IntegerField()

    def validate_url(self, value):
        user = self.context['user']
        link = '/'.join(value.rsplit('/', 2)[-2:])
        image_url = Image.objects.filter(url=link, author=user)

        if not image_url:
            raise serializers.ValidationError('We cannot find link to original image!')
        return value
