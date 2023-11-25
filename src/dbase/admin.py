from django.contrib import admin
from django.utils.html import format_html

from .models import User, Food, Expectation_Courier, Courier, Statistics, NewOrders, DeliveryOrders, Business, FeedBack
from django import forms
from django.contrib.auth.models import Group
from django.contrib.admin.models import LogEntry


class FoodModelForm(forms.ModelForm):
    structure = forms.CharField(widget=forms.Textarea, label='Состав блюда', help_text='Напишите из чего состоит блюдо')
    CHOICES = (
        ('Первое блюдо', 'Первое блюдо'),
        ('Второе блюдо', 'Второе блюдо'),
        ('Салаты', 'Салаты'),
        ('Десерты', 'Десерты'),
        ('Напиток', 'Напиток'),

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
    list_display = ('id_user', "username_telegtam", "name")
    readonly_fields = ('id_user', 'username_telegtam', 'name', 'number_phone', 'type_amusement', 'description')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'is_admin')
    fields = ['name', 'phone', 'is_admin']


@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ('username_telegtam', 'number_phone')
    fields = ['id_user', 'username_telegtam', 'number_phone']


@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ('food_name', 'count', 'remained', 'price', 'day_of_the_week', 'date')


@admin.register(NewOrders)
class NewOrdersAdmin(admin.ModelAdmin):

    def delete_button(self, obj):
        return format_html('<a class="btn" href="/admin/dbase/neworders/{}/delete/">Заказ выполнен</a>', obj.id_order)

    list_display = ('id_order', 'user_name', 'user_phone', 'price', 'foods', 'delivery', 'floor', 'delete_button')


@admin.register(DeliveryOrders)
class DeliveryOrdersAdmin(admin.ModelAdmin):
    list_display = ('id_order', 'courier_username', 'courier_phone')


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'count')
    fields = ['title', 'photo', 'price', 'count', 'first_dish', 'second_dish', 'third_dish', 'fours_dish', 'fives_dish',
              'structure']


@admin.register(FeedBack)
class Expectation_CourierAdmin(admin.ModelAdmin):
    list_display = ("username", "food_title", 'description', 'stars')
    readonly_fields = ("username", "food_title", 'description', 'stars')


admin.site.unregister(Group)