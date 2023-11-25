from django import forms


class Delivery(forms.Form):
    check = forms.BooleanField(required=False, label="Доставить заказ?")
    floor = forms.CharField(required=False, label='На какой этаж вам осуществить доставку?', max_length=120)