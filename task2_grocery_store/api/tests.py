from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from carts.models import Cart, CartItem
from categories.models import Category, Subcategory
from products.models import Product

User = get_user_model()


class ApiTests(TestCase):
    '''Тестирование GET и POST-запросов к страницам приложения'''

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='password123'
        )
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.category = Category.objects.create(
            name='test_category_name', 
            slug='test_category_slug'
        )
        self.subcategory = Subcategory.objects.create(
            category=self.category,
            name='test_subcategory_name',
            slug='test_subcategory_slug'
        )
        self.product = Product.objects.create(
            name='test_product_name',
            slug='test_product_slug',
            category=self.category,
            subcategory=self.subcategory,
            price='100.00'
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=1
        )

    def test_urls_guest_client(self):
        '''
        Проверка доступа к открытым страницам у неавторизованного пользователя
        '''

        pages = (
            '/api/categories/',
            f'/api/categories/{self.category.id}/',
            '/api/products/',
            f'/api/products/{self.product.id}/',
        )
        for page in pages:
            response = self.guest_client.get(page)
            error_name = f'Ошибка: нет доступа до страницы {page}'
            self.assertEqual(response.status_code, 200, error_name)

    def test_get_token(self):
        '''Тестирование POST-запроса к странице /api/token/'''

        data = {
            "username": "testuser",
            "password": "password123"
        }
        response = self.authorized_client.post('/api/token/', data)
        self.assertEqual(response.status_code, 200)
