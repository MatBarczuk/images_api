import shutil

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from images.models import Image, Thumbnail

TEST_DIR = 'test_data'


class ImageTest(TestCase):

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass123')
        self.image = Image.objects.create(
            author=self.user,
            url=SimpleUploadedFile('test_file.jpg', b'test file content')
        )

    def test_image_fields(self):
        self.assertEqual(
            [*self.image.__dict__],
            ['_state', 'id', 'author_id', 'url', 'name', 'created_at', 'updated_at']
        )

    def test_image_creation(self):
        self.assertTrue(isinstance(self.image, Image))
        self.assertEqual(self.image.author, self.user)
        self.assertEqual(self.image.url.url, '/media/images/test_file.jpg')
        self.assertEqual(self.image.name, 'test_file.jpg')
        self.assertEqual(self.image.__str__(), 'test_file.jpg')


class ThumbnailTest(TestCase):

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass123')
        self.image = Image.objects.create(
            author=self.user,
            url=SimpleUploadedFile('test_file.jpg', b'test file content')
        )
        self.thumbnail = Thumbnail.objects.create(
            image=self.image,
            url=SimpleUploadedFile('test_resized_file.jpg', b'test file content'),
            height=200
        )

    def test_thumbnail_fields(self):
        self.assertEqual(
            [*self.thumbnail.__dict__],
            ['_state', 'id', 'image_id', 'url', 'height']
        )

    def test_image_creation(self):
        self.assertTrue(isinstance(self.thumbnail, Thumbnail))
        self.assertEqual(self.thumbnail.image, self.image)
        self.assertEqual(self.thumbnail.url.url, '/media/resized_images/test_resized_file.jpg')
        self.assertEqual(self.thumbnail.height, 200)
        self.assertEqual(self.thumbnail.__str__(), 'resized_images/test_resized_file.jpg')


def tearDownModule():
    try:
        shutil.rmtree(TEST_DIR)
    except OSError:
        pass
