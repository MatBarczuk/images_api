from django.test import TestCase

from tiers.models import Size, Tier


class TierTest(TestCase):

    def setUp(self):
        self.tier = Tier.objects.create(
            name='test tier'
        )
        self.size = Size.objects.create(height=200)
        self.tier.size.add(self.size)

    def test_tier_fields(self):
        self.assertEqual(
            [*self.tier.__dict__],
            ['_state', 'id', 'name', 'link_flag', 'expired_link_flag']
        )

    def test_tier_creation(self):
        self.assertTrue(isinstance(self.tier, Tier))
        self.assertEqual(self.tier.name, 'test tier')
        self.assertEqual(self.tier.link_flag, False)
        self.assertEqual(self.tier.expired_link_flag, False)
        self.assertEqual(self.tier.__str__(), 'test tier')


class SizeTest(TestCase):

    def setUp(self):
        self.size = Size.objects.create(height=200)

    def test_size_fields(self):
        self.assertEqual(
            [*self.size.__dict__],
            ['_state', 'id', 'height']
        )

    def test_size_creation(self):
        self.assertTrue(isinstance(self.size, Size))
        self.assertEqual(self.size.height, 200)
        self.assertEqual(self.size.__str__(), '200 px')
