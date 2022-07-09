import pytest
from django.urls import reverse

from shop.models import Category, Product, Type, Cart, ProductCart, ProductTenderRequest
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_product_create(client, category, type):
    """Dodawanie produktów do bazy danych"""
    category = Category.objects.first()
    type = Type.objects.first()
    x = Product.objects.count()
    Product.objects.create(name="TestProduct", description="lorem ipsum", available=True, category=category,
                           type=type)
    y = Product.objects.count()
    assert x == y - 1


@pytest.mark.django_db
def test_user_create():
    """Tworzenie użytkownika"""
    x = User.objects.count()
    User.objects.create_user('test', 'test@test', 'test')
    y = User.objects.count()
    assert x == y - 1


@pytest.mark.django_db
def test_set_password(user):
    """Zmiana hasła"""
    user.set_password("new_password")
    assert user.check_password("new_password") is True


@pytest.mark.django_db
def test_set_user(user):
    """Zwykły użytkownik"""
    assert user.username == "test-user"


def test_new_user(new_user):
    """Zwykły użytkownik"""
    assert new_user.first_name == "MyName"


def test_new_staff_user(new_staff_user):
    """Użytkownik obsługi sklepu"""
    assert new_staff_user.is_staff


def test_an_admin_view(admin_client):
    """Admin"""
    response = admin_client.get('/admin/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_all_products_view(client, product):
    """Wszystkie produkty na stronie głównej"""
    url = reverse('product_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['products'].first() == product


@pytest.mark.django_db
def test_all_category_products_view(client, category):
    """Wszystkie kategorie na stronie głównej"""
    url = reverse('product_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['categories'].first() == category


@pytest.mark.django_db
def test_category_products_view(client, product):
    """Wszystkie produkty w danej kategorii"""
    slug = Category.objects.first().slug
    response = client.get(f"/category/{slug}/")
    assert response.status_code == 200
    assert response.context['products'].first() == product


@pytest.mark.django_db
def test_product_details_view(client, product):
    """Szczegóły produktu"""
    slug = Product.objects.first().slug
    response = client.get(f"/product/{slug}/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_cart_add_product_logged_view(client, product, cart):
    """Użytkownik Zalogowany, widok Szczegółów produktu"""
    client.force_login(cart.user)
    data_form = {'quantity': '100', "product_slug": product.slug}
    post_response = client.post(reverse("cart_add"), data_form, follow=True)
    assert post_response.status_code == 200


@pytest.mark.django_db
def test_cart_add_product_view(client, product):
    """Użytkownik Nie Zalogowany, widok Szczegółów produktu"""
    data_form = {'quantity': '100', "product_slug": product.slug}
    post_response = client.post(reverse("cart_add"), data_form)

    assert post_response.status_code == 302
    assert post_response.headers.get('Location') == '/login/?next=/cart_add/'
    assert post_response.url == '/login/?next=/cart_add/'
    # post_response na follow=True
    # assert post_response.status_code == 200
    # assert post_response.redirect_chain[0][0] == '/login/?next=/cart_add/'


@pytest.mark.django_db
def test_cart_update_product_view(client, cart):
    """Zalogowany, zmiana ilości produktu w koszyku"""
    client.force_login(cart.user)
    data_form = {'quantity': '20', "product_id": cart.products_list.first().id}
    post_response = client.post(reverse("cart_update"), data_form)
    assert post_response.status_code == 302
    assert ProductCart.objects.get(quantity=20)


@pytest.mark.django_db
def test_cart_details_view(client, cart):
    """Zalogowany, produktu w koszyku"""
    client.force_login(cart.user)
    url = reverse('cart_details')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["product_in_cart"].count() == cart.productcart_set.all().count()
    for pc in cart.productcart_set.all():
        assert pc in response.context["product_in_cart"]


@pytest.mark.django_db
def test_cart_delete_product_view(client, cart):
    """Zalogowany, usuwanie produktu z koszyka"""
    client.force_login(cart.user)
    x = ProductCart.objects.count()
    ProductCart.objects.first().delete()
    y = ProductCart.objects.count()
    assert x - 1 == y


@pytest.mark.django_db
def test_send_tender_request_get_view(client, cart):
    """Zalogowany, wyświetlanie zapytania"""
    client.force_login(cart.user)
    url = reverse("send_tender_request")
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["product_in_tender"].count() == 1


@pytest.mark.django_db
def test_send_tender_request_post_view(client, cart):
    """Zalogowany, wysyłanie zapytania"""
    client.force_login(cart.user)
    x = ProductTenderRequest.objects.count()
    url = reverse("send_tender_request")
    data_form = {'customer_message': 'blabla'}
    response = client.post(url, data_form)
    y = ProductTenderRequest.objects.count()
    assert response.status_code == 302
    assert response.url == reverse("success")
    assert x == y - 1


@pytest.mark.django_db
def test_success_view(client, user):
    """Zalogowany, zapytanie wysłane"""
    client.force_login(user)
    url = reverse("success")
    response = client.get(url)
    assert response.status_code == 200
