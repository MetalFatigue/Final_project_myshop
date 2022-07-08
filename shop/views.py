from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from shop import forms
from shop.models import Profil, Category, Product, Cart, ProductCart, TenderRequest, ProductTenderRequest


class SignUpView(SuccessMessageMixin, generic.CreateView):
    template_name = 'user_form.html'
    form_class = forms.UserForm
    success_message = "Dodano użytkownika"
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        profil = Profil.objects.create(company=form.cleaned_data['company'], user=self.object)
        return response


class AllProductsView(View):
    def get(self, request):
        categories = Category.objects.all()
        products = Product.objects.all()
        return render(request, 'product_list.html', {'categories': categories, 'products': products})


class CategoryProductsView(View):
    def get(self, request, category_slug):
        category = Category.objects.get(slug=category_slug)
        products = Product.objects.filter(available=True, category=category)
        categories = Category.objects.all()
        return render(request, 'product_list_by_category.html', {'category': category, 'products': products, 'categories': categories})


class ProductDetailView(View):
    def get(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug, available=True)
        categories = Category.objects.all()
        return render(request, 'product_details.html', {'categories': categories, 'product': product})


class CartAddProductView(View):
    def post(self, request):
        quantity = request.POST.get("quantity")
        product_slug = request.POST.get("product_slug")
        product = Product.objects.get(slug=product_slug)
        cart, created = Cart.objects.get_or_create(user=request.user)
        pc,created = ProductCart.objects.get_or_create(cart=cart, product=product)
        pc.quantity = quantity
        pc.save()
        return redirect('cart_details')


class CartUpdateProductView(View):
    def post(self, request):
        quantity = request.POST.get("quantity")
        product_id = request.POST.get("product_id")
        product = Product.objects.get(id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        pc = ProductCart.objects.get(cart=cart, product=product)
        pc.quantity = quantity
        pc.save()
        return redirect('cart_details')


class CartDetailsView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        product_in_cart = ProductCart.objects.filter(cart=cart)
        return render(request, 'cart_details.html', {"product_in_cart": product_in_cart})


class CartDeleteView(SuccessMessageMixin, generic.DeleteView):
        model = ProductCart
        success_url = reverse_lazy('cart_details')
        template_name = 'product_cart_delete.html'
        success_message = "Usunięto"


class SendTenderRequestView(View):
    def get(self, request):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        product_in_tender = ProductCart.objects.filter(cart=cart)
        return render(request, 'tender_details.html', {"product_in_tender": product_in_tender})

    def post(self, request):
        user = request.user
        cart = Cart.objects.get(user=user)
        product_list = ProductCart.objects.filter(cart=cart)
        customer_message = request.POST.get("customer_message")
        tender_request = TenderRequest.objects.create(user=user, customer_message=customer_message)
        for pc in product_list:
            ProductTenderRequest.objects.create(tender_request=tender_request, product=pc.product, quantity=pc.quantity)

        return redirect('success')


class SuccessView(View):
    def get(self, request):
        message = "Zapytanie zostało wysłane"
        return render(request, 'success.html', {"message": message})
