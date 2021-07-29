from rest_framework import serializers

from expiring_links.models import ExpiringLink
from images.models import Image


class ExpiringLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = ('url', 'expiration_date')


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
