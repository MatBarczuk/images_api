from rest_framework import serializers

from images.models import Image, Thumbnail


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Image


class ThumbnailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('image', 'url')
        model = Thumbnail


class ThumbnailGeneratorSerializer(serializers.Serializer):
    image = serializers.URLField()
    heights = serializers.ListField()

    def validate_heights(self, value):
        user = self.context['user']
        available_heights = [size.height for size in user.tier.size.all()]
        for height in value:
            if not isinstance(height, int):
                raise serializers.ValidationError(f'Height ({height}) is not an Integer.')
            if not height > 0:
                raise serializers.ValidationError(f'Height ({height}) must be greater than 0.')
            if height not in available_heights:
                raise serializers.ValidationError(
                    f'Chosen height ({height}) is not available in your tier ({user.tier}).')

        return value
