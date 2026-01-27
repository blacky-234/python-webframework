from django.test import TestCase,Client
from django.core.cache import cache
from products.models import Category
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class ListCategoryCacheTest(TestCase):

    def setup(self):
       
        self.client = Client()
        cache.clear()
        Category.objects.create(name="test")
    

    def test_list_category_cache(self):

        #step1 : First Request Catch
        response1 = self.client.get("/products/category/list/")
        print(response1)
        self.assertEqual(response1.status_code,200)

         # step2 : extract queryset
        categories = response1.context["categories"]

        # step3 : check length
        print("categories ===>", categories)
        print("length ===>", len(categories))

        # ASSERT LENGTH
        if(self.assertEqual(len(categories), 1)):
            print("Success")
        else:
            self.fail("Failed")



class ListCategoryMenuTest(StaticLiveServerTestCase):

    def setUp(self):

        self.selenium = webdriver.Chrome()
        self.selenium.implicitly_wait(10)
    

    def tearDown(self):
        self.selenium.quit()
        return super().tearDown()