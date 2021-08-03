import shutil

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from expiring_links.serializers import ExpiringLinkGeneratorSerializer
from images.models import Image

TEST_DIR = 'test_data'


class ExpiringLinkGeneratorSerializerTest(TestCase):

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass123')
        self.image = Image.objects.create(
            author=self.user,
            url=SimpleUploadedFile('test_file.jpg', b'test file content')
        )
        self.serializer_data = {
            'url': f'http://0.0.0.0:8000/media/{self.image.url.url}',
            'expiration_time': 30
        }
        self.serializer = ExpiringLinkGeneratorSerializer(data=self.serializer_data, context={'user': self.user})

    def test_valid_serializer(self):
        self.assertTrue(self.serializer.is_valid())

    def test_fields(self):
        self.assertCountEqual(self.serializer_data.keys(), ['url', 'expiration_time'])

    def test_wrong_url(self):
        self.serializer_data['url'] = 'http://0.0.0.0:8000/media/images/wrong_test_file.jpg'

        serializer = ExpiringLinkGeneratorSerializer(data=self.serializer_data, context={'user': self.user})

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'url'})


def tearDownModule():
    try:
        shutil.rmtree(TEST_DIR)
    except OSError:
        pass
