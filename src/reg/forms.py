from django import forms
from dbase import models
from phonenumber_field.modelfields import PhoneNumberField


class RegisterCompany(forms.Form):
    title = forms.CharField(max_length=120, help_text='Введите название команды')
    adresses = forms.CharField(max_length=10000, help_text='Введите все адреса вашей компании. Каждый адрес вводите на новой строке')
    balance = forms.IntegerField(help_text='Введите стоимость заказа пользователя')

    class Meta:
        model = models.Company
        fields = ['title', 'address', 'balance', 'image']


class RegisterUser(forms.Form):
    name = forms.CharField(max_length=120, help_text='Введите ваше имя')
    password = forms.CharField(max_length=10000, help_text='Придумайте пароль')
    phone = forms.RegexField(regex=r'^\+?1?\d{9,15}$')

    class Meta:
        model = models.User
        fields = ['name', 'password', 'phone']


class LoginUser(forms.Form):
    phone = forms.RegexField(regex=r'^\+?1?\d{9,15}$', help_text='Введите номер телефона')
    password = forms.CharField(max_length=10000, help_text='Введите пароль')

    class Meta:
        model = models.User
        fields = ['phone', 'password']