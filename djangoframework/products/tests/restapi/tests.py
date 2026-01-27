from rest_framework.test import APITestCase
from django.urls import reverse
from products.models import Category

class ProductManagement(APITestCase):
    def setUp(self):
        Category.objects.create(name="Electronics")
        Category.objects.create(name="Books")
    def test_get_product(self):

        url = reverse('products:productmanagement')
        response = self.client.get(url)
        print("what is urls : ",response)
        print(f"status code : {response.status_code}")
        print(f"Raw content : {response.content}")
        print(f"response json data : {response.json()}")
        self.assertGreaterEqual(len(response.json()),1)