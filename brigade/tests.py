from django.test import TestCase
from django.core.urlresolvers import reverse

from rest_framework.test import APIClient
from rest_framework import status

from .models import Brigade
from user.models import MyUser

from custom_jwt import create_token


class BrigadeViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        director = MyUser.objects.create_director(
            username='director', password='director'
        )
        token = create_token(director)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        self.brigade_data = {'name': 'Lorem'}
        self.response = self.client.post(
            reverse('core:brigade-list'),
            self.brigade_data,
            format="json")

    def test_api_can_create_a_brigade(self):
        """Test the api has brigade creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_a_brigade(self):
        """Test the api can get a given brigade."""
        brigade = Brigade.objects.get()
        response = self.client.get(
            reverse('core:brigade-detail', kwargs={'brigade_id': brigade.id}),
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, brigade)

    def test_api_can_update_brigade(self):
        """Test the api can update a given brigade."""
        brigade = Brigade.objects.get()
        change_brigade = {'name': 'Something new'}
        response = self.client.put(
            reverse('core:brigade-detail', kwargs={'brigade_id': brigade.id}),
            change_brigade,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_can_delete_brigade(self):
        """Test the api can delete a brigade."""
        brigade = Brigade.objects.get()
        response = self.client.delete(
            reverse('core:brigade-detail', kwargs={'brigade_id': brigade.id}),
            format='json',
            follow=True
        )

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
