import pytest
from django.urls import reverse

from shop.models import Category, Product, Type
from django.contrib.auth.models import User


@pytest.fixture
def setup():
    category = Category.objects.create(name='TestCategory')
    product_type = Type.objects.create(name='TestType')


@pytest.mark.django_db
def test_Product_Add(client, setup):
    category = Category.objects.first()
    product_type = Type.objects.first()
    x = Product.objects.count()
    Product.objects.create(name="TestProduct", description="lorem ipsum", available=True, category=category,
                           type=product_type)
    y = Product.objects.count()
    assert x == y - 1


@pytest.mark.django_db
def test_user_create():
    x = User.objects.count()
    User.objects.create_user('test', 'test@test', 'test')
    y = User.objects.count()
    assert x == y - 1


@pytest.fixture
def user_1(db):
    return User.objects.create_user("test-user")


@pytest.mark.django_db
def test_set_password(user_1):
    user_1.set_password("new_password")
    assert user_1.check_password("new_password") is True


@pytest.mark.django_db
def test_set_user(user_1):
    assert user_1.username == "test-user"


def test_new_user(new_user):
    assert new_user.first_name == "MyName"


def test_new_staff_user(new_staff_user):
    assert new_staff_user.is_staff


@pytest.fixture
def category():
    category = Category.objects.create(name='TestCategory')
    return category


@pytest.fixture
def type():
    type = Type.objects.create(name='TestType')
    return type


@pytest.fixture
def product(category, type):
    p = Product.objects.create(name="TestProduct", description="lorem ipsum", available=True, category=category,
                           type=type)
    return p


@pytest.mark.django_db
def test_All_Products_View(client, product):

    url = reverse('product_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['products'].first() == product


@pytest.mark.django_db
def test_AllProductsCategoryView(client, category):
    url = reverse('product_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['categories'].first() == category


# @pytest.fixture
# def
# response


@pytest.mark.django_db
def test_CategoryProductsView(client, category):
    url = reverse("product_list_by_category", category.slug)
    response = client.get(url)
    assert response.status_code == 200
