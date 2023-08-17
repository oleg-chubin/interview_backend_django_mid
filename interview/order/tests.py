from datetime import datetime, timedelta, date

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from interview.inventory.models import Inventory, InventoryType, InventoryLanguage
from interview.order.models import Order


class OrderListTests(APITestCase):
    def setUp(self) -> None:
        inventory_type = InventoryType.objects.create(name='test')
        inventory_language = InventoryLanguage.objects.create(name='en')
        self.inventory = Inventory.objects.create(
            name='salt',
            type=inventory_type,
            language=inventory_language,
            metadata={}
        )
        self.orders = []
        offsets = [5, 3, 1]
        self.now = datetime.utcnow()
        for end in offsets:
            self.orders.append(
                Order.objects.create(
                    inventory=self.inventory,
                    start_date=self.now - timedelta(days=1),
                    embargo_date=self.now + timedelta(days=end)
                )
            )

    def test_list_orders_empty_result(self):
        """
        Ensure we can create a new account object.
        """
        for obj in Order.objects.all():
            obj.delete()

        url = reverse('order-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_orders_full_result(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('order-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.orders))

    def test_list_orders_filtered_start_result(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('order-list')
        start_date = self.now + timedelta(days=2)
        response = self.client.get(url, data={'start_date': str(start_date.date())}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len([i for i in self.orders if i.embargo_date >= start_date]))
        self.assertTrue(all(date.fromisoformat(i['embargo_date']) >= start_date.date() for i in response.data))

    def test_list_orders_filtered_end_result(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('order-list')
        end_date = self.now + timedelta(days=4)
        response = self.client.get(url, data={'end_date': str(end_date.date())}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len([i for i in self.orders if i.embargo_date <= end_date]))
        self.assertTrue(all(date.fromisoformat(i['embargo_date']) <= end_date.date() for i in response.data))

    def test_list_orders_filtered_both_result(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('order-list')
        end_date = self.now + timedelta(days=4)
        start_date = self.now + timedelta(days=2)
        response = self.client.get(
            url,
            data={'start_date': str(start_date.date()), 'end_date': str(end_date.date())},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len([i for i in self.orders if start_date <= i.embargo_date <= end_date]))
        self.assertTrue(
            all(start_date.date() <= date.fromisoformat(i['embargo_date']) <= end_date.date() for i in response.data)
        )
