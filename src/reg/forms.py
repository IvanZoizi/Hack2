from django import forms
from dbase import models


class RegisterCompany(forms.Form):
    title = forms.CharField(max_length=120, help_text='Введите название команды')
    adresses = forms.CharField(max_length=10000, help_text='Введите все адреса вашей компании. Каждый адрес вводите на новой строке')
    balance = forms.IntegerField(help_text='Введите стоимость заказа пользователя')


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