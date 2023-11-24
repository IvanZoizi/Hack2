from django.contrib import admin
from django.utils.html import format_html

from .models import User, Food, Expectation_Courier, Courier, Statistics, NewOrders, DeliveryOrders
from django import forms
from django.contrib.auth.models import Group
from django.contrib.admin.models import LogEntry


class FoodModelForm(forms.ModelForm):
    structure = forms.CharField(widget=forms.Textarea, label='Состав блюда', help_text='Напишите из чего состоит блюдо')
    CHOICES = (
        ('1', 'Первое блюдо'),
        ('2', 'Второе блюдо'),
        ('3', 'Салаты'),
        ('4', 'Десерты'),
        ('5', 'Напиток'),

    )
    type_food = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = Food
        fields = ['title', 'photo', 'price', 'structure', 'type_food', 'protein', 'fats', 'carbohydrates']


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    fields = ['title', 'photo', 'price', 'count', 'structure', 'type_food', 'protein', 'fats', 'carbohydrates']
    ordering = ['type_food']

    def change_button(self, obj):
        return format_html('<a class="btn" href="/admin/dbase/food/{}/change/">Изменить</a>', obj.id_food)

    def delete_button(self, obj):
        return format_html('<a class="btn" href="/admin/dbase/food/{}/delete/">Удалить</a>', obj.id_food)

    list_display = ("title", 'type_food', "price", 'count', 'protein', 'fats', 'carbohydrates', 'change_button', 'delete_button')

    form = FoodModelForm


@admin.register(Expectation_Courier)
class Expectation_CourierAdmin(admin.ModelAdmin):
    list_display = ("username_telegtam", "name")
    readonly_fields = ('username_telegtam', 'name', 'number_phone', 'type_amusement', 'avto', 'description')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'is_admin')
    fields = ['name', 'phone', 'is_admin']


@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ('username_telegtam', 'number_phone')
    fields = ['username_telegtam', 'number_phone']


@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ('food_name', 'count', 'price', 'day_of_the_week', 'date')


@admin.register(NewOrders)
class NewOrdersAdmin(admin.ModelAdmin):
    list_display = ('id_order', 'user_name', 'user_phone', 'price', 'foods')


@admin.register(DeliveryOrders)
class DeliveryOrdersAdmin(admin.ModelAdmin):
    list_display = ('id_order', 'courier_username', 'courier_phone')


admin.site.unregister(Group)
LogEntry.objects.all().delete()