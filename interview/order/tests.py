from datetime import datetime, timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase
from interview.inventory.models import Inventory, InventoryType, InventoryLanguage
from interview.order.models import Order


class DeactivateOrderTests(APITestCase):
    def setUp(self) -> None:
        inventory_type = InventoryType.objects.create(name='test')
        inventory_language = InventoryLanguage.objects.create(name='en')
        inventory = Inventory.objects.create(
            name='salt',
            type=inventory_type,
            language=inventory_language,
            metadata={}
        )
        self.order = Order.objects.create(
            inventory=inventory,
            start_date=datetime.utcnow() - timedelta(days=1),
            embargo_date=datetime.utcnow() + timedelta(days=1)
        )
        self.salt_order = Order.objects.create(
            inventory=inventory,
            start_date=datetime.utcnow() - timedelta(days=1),
            embargo_date=datetime.utcnow() + timedelta(days=1)
        )

    def test_deactivate_unexisting_order(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('order-deactivate', kwargs={'pk': max(self.salt_order.id, self.order.id) + 1})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='Not found.', code='not_found')})

    def test_deactivate_existing_order(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('order-deactivate', kwargs={'pk': self.order.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)

    def test_deactivate_inactive_order(self):
        """
        Ensure we can create a new account object.
        """
        self.order.deactivate(self.order.pk)
        url = reverse('order-deactivate', kwargs={'pk': self.order.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)
