import pytest
from django.urls import reverse

from shop.models import Category, Product, Type, Cart
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_Product_Add(client, category, type):
    category = Category.objects.first()
    type = Type.objects.first()
    x = Product.objects.count()
    Product.objects.create(name="TestProduct", description="lorem ipsum", available=True, category=category,
                           type=type)
    y = Product.objects.count()
    assert x == y - 1


@pytest.mark.django_db
def test_user_create():
    x = User.objects.count()
    User.objects.create_user('test', 'test@test', 'test')
    y = User.objects.count()
    assert x == y - 1


@pytest.mark.django_db
def test_set_password(user):
    user.set_password("new_password")
    assert user.check_password("new_password") is True


@pytest.mark.django_db
def test_set_user(user):
    assert user.username == "test-user"


def test_new_user(new_user):
    assert new_user.first_name == "MyName"


def test_new_staff_user(new_staff_user):
    assert new_staff_user.is_staff


def test_an_admin_view(admin_client):
    response = admin_client.get('/admin/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_All_Products_View(client, product):
    """wszystkie produkty na stronie głównej"""
    url = reverse('product_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['products'].first() == product


@pytest.mark.django_db
def test_AllProductsCategoryView(client, category):
    """wszystkie kategorie na stronie głownej"""
    url = reverse('product_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['categories'].first() == category



@pytest.mark.django_db
def test_CategoryProductsView(client, product):
    """wszystkie produkty w danej kategorii"""
    slug = Category.objects.first().slug
    response = client.get(f"/category/{slug}/")
    assert response.status_code == 200
    assert response.context['products'].first() == product


@pytest.mark.django_db
def test_ProductDetailsView(client, product):
    """Szczegóły produktu"""
    slug = Product.objects.first().slug
    response = client.get(f"/product/{slug}/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_CartAddProductLoggedView(client, product, new_user):
    """Użytkownik Zalogowany, widok Szczegółów produktu"""
    client.force_login(new_user)
    data_form = {'quantity': '100', "product_slug": product.slug}
    post_response = client.post(reverse("cart_add"), data_form, follow=True)
    assert post_response.status_code == 200


@pytest.mark.django_db
def test_CartAddProductView(client, product, new_user):
    """Użytkownik Nie Zalogowany, widok Szczegółów produktu"""
    data_form = {'quantity': '100', "product_slug": product.slug}
    post_response = client.post(reverse("cart_add"), data_form)

    assert post_response.status_code == 302
    assert post_response.headers.get('Location') == '/login/?next=/cart_add/'

    # post_response na follow=True
    # assert post_response.status_code == 200
    # assert post_response.redirect_chain[0][0] == '/login/?next=/cart_add/'


@pytest.mark.django_db
def test_CartUpdateProductLoggedView(client, product, new_user):
    """Zalogowany"""
    client.force_login(new_user)
    data_form = {'quantity': '100', "product_id": product.id}
    post_response = client.post(reverse("cart_update"), data_form)
    assert post_response.status_code == 200


@pytest.mark.django_db
def test_CartDetailsView(client, new_user):
    client.force_login(new_user)
    cart = Cart.objects.get(user=new_user)
    response = client.get('cart_details')
    assert response.status_code == 200

