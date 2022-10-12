"""myshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path

from shop import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('signup/', views.SignUpView.as_view(), name="signup"),

    path('', views.AllProductsView.as_view(), name='product_list'),
    path('category/<slug:category_slug>/', views.CategoryProductsView.as_view(), name='product_list_by_category'),
    path('product/<slug:product_slug>/', views.ProductDetailView.as_view(), name='product_details'),

    path('cart_add/', views.CartAddProductView.as_view(), name="cart_add"),
    path('cart_update/', views.CartUpdateProductView.as_view(), name="cart_update"),
    path('cart_details/', views.CartDetailsView.as_view(), name="cart_details"),
    path('cart_delete/<int:pk>/', views.CartDeleteView.as_view(), name="product_cart_delete"),

    path('send_tender_request/', views.SendTenderRequestView.as_view(), name="send_tender_request"),
    path('success/', views.SuccessView.as_view(), name="success"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
