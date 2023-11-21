from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import User, Food
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
    readonly_fields = ('photo',)

    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'Photo Preview'
    thumbnail_preview.allow_tags = True

    form = FoodModelForm


admin.site.unregister(Group)