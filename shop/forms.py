from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from shop import models


class UserForm(UserCreationForm):
    company = forms.CharField(max_length=40)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


# class CategoryForm(forms.ModelForm):
#     class Meta:
#         model = models.Category
#         fields = ['name']
#
#
# class TypeForm(forms.ModelForm):
#     class Meta:
#         model = models.Type
#         fields = ['name']
#
#
# class Product(forms.ModelForm):
#     class Meta:
#         model = models.Product
#         fields = '__all__'