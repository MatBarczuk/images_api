import shutil

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from images.models import Image, Thumbnail
from images.serializers import ImageSerializer, ThumbnailGeneratorSerializer
from tiers.models import Tier, Size

TEST_DIR = 'test_data'


class ImageSerializerTest(TestCase):

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass123')
        self.image = Image.objects.create(
            author=self.user,
            url=SimpleUploadedFile('test_file.jpg', b'test file content')
        )
        self.serializer = ImageSerializer(instance=self.image)
        self.serializer_data = self.serializer.data

    def test_fields(self):
        self.assertCountEqual(self.serializer_data.keys(), ['id', 'author', 'name', 'created_at', 'updated_at'])


class ThumbnailGeneratorSerializerTest(TestCase):

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def setUp(self):
        self.tier = Tier.objects.create(
            name='test tier'
        )
        self.size = Size.objects.create(height=200)
        self.tier.size.add(self.size)
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass123', tier=self.tier)
        self.image = Image.objects.create(
            author=self.user,
            url=SimpleUploadedFile('test_file.jpg', b'test file content')
        )
        self.thumbnail = Thumbnail.objects.create(
            image=self.image,
            url=SimpleUploadedFile('test_resized_file.jpg', b'test file content'),
            height=200
        )
        self.serializer_data = {
            'image': 'test_file.jpg',
            'heights': [200]
        }
        self.serializer = ThumbnailGeneratorSerializer(data=self.serializer_data, context={'user': self.user})

    def test_fields(self):
        self.assertCountEqual(self.serializer_data.keys(), ['image', 'heights'])

    def test_valid_serializer(self):
        self.assertTrue(self.serializer.is_valid())

    def test_wrong_image(self):
        self.serializer_data['image'] = 'fail_test_file.jpg'

        serializer = ThumbnailGeneratorSerializer(data=self.serializer_data, context={'user': self.user})

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'image'})

    def test_wrong_height_data_type(self):
        self.serializer_data['heights'] = ['not_an_int']

        serializer = ThumbnailGeneratorSerializer(data=self.serializer_data, context={'user': self.user})

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'heights'})

    def test_height_not_positive(self):
        self.serializer_data['heights'] = [0]

        serializer = ThumbnailGeneratorSerializer(data=self.serializer_data, context={'user': self.user})

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'heights'})

    def test_height_not_available(self):
        self.serializer_data['heights'] = [100]

        serializer = ThumbnailGeneratorSerializer(data=self.serializer_data, context={'user': self.user})

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'heights'})


def tearDownModule():
    try:
        shutil.rmtree(TEST_DIR)
    except OSError:
        pass
