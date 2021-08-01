from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from helpers.image_resizing import ThumbnailMakerService
from images.models import Image, Thumbnail
from images.serializers import ImageSerializer, ThumbnailGeneratorSerializer


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer

    def get_queryset(self):
        user = self.request.user
        return Image.objects.filter(author=user)


class ThumbnailViewSet(viewsets.ViewSet):
    def create(self, request):
        result = ThumbnailGeneratorSerializer(data=request.data, context={'user': request.user})
        if result.is_valid():
            heights = result.data.get('heights')
            url = result.data.get('image')
            heights_in_db = [thumbnail.height for thumbnail in Thumbnail.objects.filter(image=url)]
            generated_heights = []
            not_generated_heights = []
            for height in heights:
                if height in heights_in_db:
                    generated_heights.append(height)
                else:
                    not_generated_heights.append(height)

            tn_maker = ThumbnailMakerService(target_sizes=not_generated_heights)
            tn_maker.make_thumbnails(['/'.join(url.rsplit('/', 2)[-2:])])

            resized_link_format = url.rsplit('.', 1)
            resized_link_parts = resized_link_format[0].rsplit('/', 2)

            resized_links = []
            for height in generated_heights:
                resized_links.append(Thumbnail.objects.get(image=url, height=height).url.name)

            for height in not_generated_heights:
                resized_link = f'{resized_link_parts[0]}/resized_images/{resized_link_parts[1]}/{resized_link_parts[2]}_{height}.{resized_link_format[1]}'
                resized_links.append(resized_link)
                Thumbnail.objects.create(image=url, url=resized_link, height=height)
            return Response({'link': resized_links})
        return Response(result.errors)
