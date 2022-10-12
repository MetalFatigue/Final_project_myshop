from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class Profil(models.Model):
    """Dodatkowe pole w tabeli User"""
    company = models.CharField(max_length=30)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'profil'
        verbose_name_plural = 'profile'


class Category(models.Model):
    """Kategorie produktów"""
    name = models.CharField(max_length=200, unique=True, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'kategoria'
        verbose_name_plural = 'kategorie'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Type(models.Model):
    """Typy produktów"""
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ('name',)
        verbose_name = 'typ'
        verbose_name_plural = 'typy'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Produkty"""
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True, verbose_name='Nazwa produktu')
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    description = models.TextField(blank=True, verbose_name='Opis')
    image = models.ImageField(upload_to='products/%Y/%m/%d', null=True, blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'produkt'
        verbose_name_plural = 'produkty'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Cart(models.Model):
    """Koszyk"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products_list = models.ManyToManyField(Product, through='ProductCart')

    class Meta:
        verbose_name = 'koszyk'
        verbose_name_plural = 'koszyki'


class ProductCart(models.Model):
    """Produkty w koszyku"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)


class TenderRequest(models.Model):
    """Zapytanie ofertowe"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products_list = models.ManyToManyField(Product, through='ProductTenderRequest')
    customer_message = models.CharField(max_length=250, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    answered = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'zapytanie'
        verbose_name_plural = 'zapytania'

class ProductTenderRequest(models.Model):
    """Produkty w zapytaniu"""
    tender_request = models.ForeignKey(TenderRequest, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)

    class Meta:
        verbose_name = 'produkty z zapytania'
        verbose_name_plural = 'produkty z zapytania'


# class EmailTenderRequest(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     tender_request = models.ForeignKey(User, on_delete=models.CASCADE)
#     message = models.ForeignKey(ProductCart, on_delete=models.CASCADE)

# class Answer(models.Model):
#     product_list = models.ManyToManyField(Product, through='ProductPrices')
#     zapytanie = models.ForeignKey(ZapytanieOfertowe, on_delete=models.CASCADE)
#
# class ProductPrices(models.Model):
#     answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     price = models.FloatField()
