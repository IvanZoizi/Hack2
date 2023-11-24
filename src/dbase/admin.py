from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import User, Food, Expectation_Courier, Courier
from django import forms
from django.contrib.auth.models import Group


class FoodModelForm(forms.ModelForm):
    structure = forms.CharField(widget=forms.Textarea, label='Состав блюда', help_text='Напишите из чего состоит блюдо')

    class Meta:
        model = Food
        fields = ['title', 'photo', 'price', 'structure', 'protein', 'fats', 'carbohydrates']


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ("title", "price", 'protein', 'fats', 'carbohydrates', 'photo')
    search_fields = ('title',)
    fields = ['title', 'photo', 'price', 'structure', 'protein', 'fats', 'carbohydrates']
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


admin.site.unregister(Group)