from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ..models import Information


class TestIndexView(APITestCase):
    def setUp(self):
        super().setUp()
        self.people = Information.objects.create(name='Awais', idCard=2323232323, roll=101, )
        self.people = Information.objects.create(name='Awais123', idCard=122323232323, roll=102)

    def test_model(self):
        self.assertEqual(Information.objects.count(), 2)
