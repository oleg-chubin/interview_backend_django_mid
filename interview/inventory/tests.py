from datetime import datetime, timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from interview.inventory.models import Inventory, InventoryType, InventoryLanguage


class InventoryListTests(APITestCase):
    def setUp(self) -> None:
        self.inventory_type = InventoryType.objects.create(name='test')
        self.inventory_language = InventoryLanguage.objects.create(name='en')

    def test_list_inventory_empty_result(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('inventory-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_inventory_full_result(self):
        """
        Ensure we can create a new account object.
        """
        names = ['a', 'b', 'c']
        for n in names:
            Inventory.objects.create(name=n, type=self.inventory_type, language=self.inventory_language, metadata={})
        url = reverse('inventory-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(names))
        self.assertEqual(sorted(names), sorted(i['name'] for i in response.data))

    def test_list_inventory_filtered_result(self):
        """
        Ensure we can create a new account object.
        """
        now = datetime.now()
        names = ['a', 'b', 'c']
        for n in names:
            Inventory.objects.create(name=n, type=self.inventory_type, language=self.inventory_language, metadata={})

        salt = Inventory.objects.create(
            name='salt',
            type=self.inventory_type,
            language=self.inventory_language,
            metadata={}
        )
        salt.created_at = now-timedelta(days=1)
        salt.save()

        url = reverse('inventory-list')
        response = self.client.get(url, data={'start_date': str(now.date())}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(names))
        self.assertEqual(sorted(names), sorted(i['name'] for i in response.data))
