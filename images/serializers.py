from rest_framework import serializers

from images.models import Image, Thumbnail


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Image


class ThumbnailGeneratorSerializer(serializers.Serializer):
    image = serializers.CharField(max_length=200)
    heights = serializers.ListField()

    def validate_image(self, value):
        user = self.context['user']
        image_name = Image.objects.filter(name=value, author=user)

        if not image_name:
            raise serializers.ValidationError(f'There is no image with this name {value}')
        return value

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
