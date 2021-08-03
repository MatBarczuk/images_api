from datetime import datetime
from uuid import uuid4, UUID

from django.test import TestCase

from expiring_links.models import ExpiringLink


class ExpiringLinkTest(TestCase):

    def setUp(self):
        self.expiring_link = ExpiringLink(
            url='http://test_link.com',
            token=uuid4(),
            expiration_date=datetime(2021, 10, 2, 15, 30)
        )

    def test_expiring_link_fields(self):
        self.assertTrue(
            [*self.expiring_link.__dict__],
            ['_state', 'id', 'url', 'token', 'expiration_date']
        )

    def test_expiring_link_creation(self):
        self.assertTrue(isinstance(self.expiring_link, ExpiringLink))
        self.assertEqual(self.expiring_link.url, 'http://test_link.com')
        self.assertTrue(isinstance(self.expiring_link.token, UUID))
        self.assertEqual(self.expiring_link.expiration_date, datetime(2021, 10, 2, 15, 30))
        self.assertEqual(self.expiring_link.__str__(), 'http://test_link.com')
