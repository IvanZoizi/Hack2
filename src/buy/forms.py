from django import forms


class Delivery(forms.Form):
    check = forms.BooleanField(required=True, label="Доставить заказ?")