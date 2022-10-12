import pytest
from django.test import Client
from shop.models import Category, Product, Type


@pytest.fixture
def setup1():
    category = Category.objects.create(name='TestCategory')
    product_type = Type.objects.create(name='TestType')


@pytest.mark.django_db
def test_Product_Add(client, setup1):
    category = Category.objects.first()
    product_type = Type.objects.first()
    x = Product.objects.count()
    Product.objects.create(name="TestProduct", description="lorem ipsum", available=True, category=category, type=product_type)
    y = Product.objects.count()
    assert x == y-1


@pytest.mark.django_db
def test_All_Products_View(client, setup1):
    response = client.get('/')
    assert response.status_code == 200
    assert response.context['products'].first() == product


@pytest.mark.django_db
def test_AllProductsCategoryView(client, category):
    response = client.get('')
    assert response.status_code == 200
    assert response.context['categories'].first() == category