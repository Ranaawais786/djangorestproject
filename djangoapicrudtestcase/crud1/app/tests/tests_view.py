from model_bakery import baker
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ..models import Information


class TestIndexView(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = baker.make(Information, name='Awais',roll=101)
        self.user = baker.make(Information, name='Usman',roll=103)
        self.user = baker.make(Information, name='azam', roll=104)



    def test_information_post_view(self):
        data = {'name': 'azam', 'idCard': 12212121, 'roll': 121}
        response = self.client.post('/first/crud/', data)

        self.assertEqual(response.status_code, 201)

    def test_information_list_view(self):
        response = self.client.get(reverse('first:test-list'))
        self.assertEqual(Information.objects.count(), 3)
        self.assertEqual(response.status_code, 200)

    def test_information_filterlist_view(self):
        response = self.client.get('http://127.0.0.1:8000/first/crud/?name=Awais')
        self.assertEqual(response.status_code, 200)

    # def test_information_filterlist1_view(self):
    #     a = 'Awais'
    #     response = self.client.get('%s?name=%s' % (reverse('first:test-list'), a))
    #     e = Information.objects.values('name')
    #
    #     self.assertEqual()
    #
    def test_information_detail_view(self):

        response = self.client.get(reverse('first:test-detail', kwargs={'pk': 2}))

        self.assertEqual(response.status_code, 200)

    def test_information_update_view(self):
        data = {'name': 'azam', 'idCard': 12212121, 'roll': 121}
        response = self.client.put(reverse('first:test-detail', kwargs={'pk': 2}), data)

        self.assertEqual(response.status_code, 200)

    def test_information_delete_view(self):
        data = {'name': 'azam', 'idCard': 12212121, 'roll': 121}
        response = self.client.delete(reverse('first:test-detail', kwargs={'pk': 2}), data)

        self.assertEqual(response.status_code, 204)
