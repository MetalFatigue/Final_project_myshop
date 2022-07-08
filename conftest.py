import pytest
from django.contrib.auth.models import User
from shop.models import Category, Type, Product, Cart, TenderRequest, ProductCart, ProductTenderRequest


@pytest.fixture
def new_user_factory(db):
    def create_app_user(
            username: str,
            password: str = None,
            first_name: str = "firstname",
            last_name: str = "lastname",
            email: str = "test@test.com",
            is_staff: str = False,
            is_superuser: str = False,
            is_active: str = True,
    ):
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
        )
        return user
    return create_app_user

@pytest.fixture
def new_user(db, new_user_factory):
    return new_user_factory("test_user", "password", "MyName")

@pytest.fixture
def new_staff_user(db, new_user_factory):
    return new_user_factory("test_user", "password", "MyName", is_staff='True')

@pytest.fixture
def user(db):
    user = User.objects.create_user("test-user")
    return user

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
    product = Product.objects.create(name="TestProduct", description="lorem ipsum", available=True, category=category, type=type)
    return product

@pytest.fixture
def product_list(product):
    product_list = []
    product_list.append(product)
    return product_list


@pytest.fixture
def cart(user, product_list):
    cart = Cart.objects.create(user=user)
    for product in product_list:
        ProductCart.objects.create(cart=cart, product=product, quantity=3)
    return cart


@pytest.fixture
def tender_request(user, product_list):
    tender_request = TenderRequest.objects.create(user=user)
    for product in product_list:
        ProductTenderRequest.objects.create(cart=cart, product=product, quantity=3)
    return tender_request
