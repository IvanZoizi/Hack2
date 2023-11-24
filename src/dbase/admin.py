from django.contrib import admin

from .models import User, Food, Expectation_Courier, Courier, Statistics, NewOrders, DeliveryOrders
from django import forms
from django.contrib.auth.models import Group


class FoodModelForm(forms.ModelForm):
    structure = forms.CharField(widget=forms.Textarea, label='Состав блюда', help_text='Напишите из чего состоит блюдо')

    class Meta:
        model = Food
        fields = ['title', 'photo', 'price', 'structure', 'protein', 'fats', 'carbohydrates']


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ("title", "price", 'count', 'protein', 'fats', 'carbohydrates')
    search_fields = ('title',)
    fields = ['title', 'photo', 'price', 'count', 'structure', 'protein', 'fats', 'carbohydrates']
    #readonly_fields = ('photo',)

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'Photo Preview'
    thumbnail_preview.allow_tags = True

    form = FoodModelForm


@admin.register(Expectation_Courier)
class Expectation_CourierAdmin(admin.ModelAdmin):
    list_display = ("username_telegtam", "name")
    readonly_fields = ('username_telegtam', 'name', 'number_phone', 'type_amusement', 'avto', 'description')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'is_staff', 'is_admin')
    fields = ['name', 'phone', 'is_staff', 'is_admin']


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