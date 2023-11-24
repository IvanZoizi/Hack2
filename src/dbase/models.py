from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, UserManager
from django.urls import reverse
from django.utils.html import format_html
from sorl.thumbnail import get_thumbnail


class UserAccountManager(UserManager):
    def create_user(self, phone, name=None, password=None, **extra_fields):
        if not phone or not name or not password:
            return ValueError("Нету аргумента")
        user = self.model(
            phone=phone,
            name=name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, name=None, password=None, **extra_fields):
        if not phone or not name:
            return ValueError('Не переданы аргументы')
        user = self.create_user(phone, name, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



class Food(models.Model):
    id_food = models.IntegerField(primary_key=True)
    photo = models.ImageField(verbose_name='Фотография блюда', upload_to='post', null=True, blank=True)

    @property
    def thumbnail_preview(self):
        if self.photo:
            _thumbnail = get_thumbnail(self.photo,
                                       '300x300',
                                       upscale=False,
                                       crop=False,
                                       quality=100)
            return format_html(
                '<img src="{}" width="{}" height="{}">'.format(_thumbnail.url, _thumbnail.width, _thumbnail.height))
        return ""

    title = models.CharField(max_length=120, verbose_name='Название блюда', help_text='Введите название блюда')
    price = models.IntegerField(verbose_name='Цена за блюдо', help_text='Введите цену за блюдо')
    count = models.IntegerField(verbose_name='Кол-во порций', help_text='Введите какое кол-во порций будет приготовлено', default=0)
    structure = models.CharField(max_length=1000, verbose_name='Состав', help_text='Напишите из чего состоит блюдо')
    protein = models.FloatField(verbose_name='Белок', help_text='Укажите сколько содержится белков в блюде в граммах')
    fats = models.FloatField(verbose_name='Жиры', help_text='Укажите сколько содержится жиров в блюде в граммах')
    carbohydrates = models.FloatField(verbose_name='Углеводы',
                                      help_text='Укажите сколько содержится углеводов в блюде')
    type_food = models.CharField(verbose_name='Вид блюда', max_length=120, help_text='Укажите вид блюда')
    objects = UserAccountManager()

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def get_absolute_url(self):
        return reverse('food', args=[self.id_food])

    def __str__(self):
        return self.title


class User(AbstractBaseUser):
    id = models.IntegerField(primary_key=True)
    phone = models.CharField(max_length=120, verbose_name='Номер телефона', help_text='Введите ваш номер телефона',
                             unique=True)
    name = models.CharField(max_length=120, verbose_name='Имя', help_text='Ваше имя и фамилию')
    password = models.CharField(max_length=120, verbose_name='Пароль пользователя', help_text='Введите ваш пароль')
    address = models.CharField(max_length=120, verbose_name='Адрес', help_text='Введите ваш адрес')
    is_staff = models.BooleanField(default=True, verbose_name='Пользователь является ')
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False, verbose_name='Пользователь является админом')

    objects = UserAccountManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['password', 'name']

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'
        db_table = 'user'
        ordering = ['id']

    def __str__(self):
        return self.phone

    def get_absolute_url(self):
        return reverse('user-info', args=[str(self.phone)])

    def get_full_name(self):
        return self.name

    def natural_key(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Statistics(models.Model):
    food_name = models.CharField(verbose_name='Название блюда', max_length=120)
    count = models.IntegerField(verbose_name='Сколько порций было куплено')
    price = models.IntegerField(verbose_name='Прибыль без учета себестоимости')
    day_of_the_week = models.CharField(verbose_name='День недели', max_length=120)
    date = models.CharField(verbose_name='Дата', max_length=120)

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'


class NewOrders(models.Model):
    id_order = models.IntegerField(verbose_name='Номер заказа')
    # id_food = models.IntegerField(verbose_name='Id блюда')
    user_name = models.CharField(verbose_name='Имя пользователя', max_length=120)
    user_phone = models.CharField(verbose_name='Номер телефона пользователя', max_length=120)
    price = models.IntegerField(verbose_name='Цена заказа')
    foods = models.CharField(verbose_name='Название блюд', max_length=12000)
    delivery = models.BooleanField(verbose_name='Доставляется ли заказ?')

    class Meta:
        verbose_name = 'Новые заказы'
        verbose_name_plural = 'Новые заказы'


class Courier(models.Model):
    number_phone = models.CharField(verbose_name='Номер телефона', max_length=12)
    username_telegtam = models.CharField(verbose_name='Username курьера в Telegram', max_length=120)

    object = models.Manager()

    def get_absolute_url(self):
        return reverse('courier', args=[self.username_telegtam])

    def __str__(self):
        return self.username_telegtam

    class Meta:
        verbose_name = 'Курьеры'
        verbose_name_plural = 'Курьеры'


class Expectation_Courier(models.Model):
    username_telegtam = models.CharField(verbose_name='Username курьера в Telegram', max_length=120)
    name = models.CharField(verbose_name='Ваше имя', max_length=120)
    number_phone = models.CharField(verbose_name='Номер телефона', max_length=12)
    type_amusement = models.CharField(verbose_name='Тип занятности', max_length=120)
    description = models.CharField(verbose_name='Расскажите о себе', max_length=3000000)

    object = models.Manager()

    def get_absolute_url(self):
        return reverse('courier', args=[self.username_telegtam])

    def __str__(self):
        return self.username_telegtam

    class Meta:
        verbose_name = 'Заявки для работы на должность "Курьер"'
        verbose_name_plural = 'Заявки для работы на должность "Курьер"'


class DeliveryOrders(models.Model):
    id_order = models.IntegerField(verbose_name='Id заказа')
    courier_username = models.CharField(max_length=120, verbose_name='Username курьера в Telegram')
    courier_phone = models.CharField(verbose_name='Номер телефона', max_length=12)

    class Meta:
        verbose_name = 'Заказы, которые доставит курьер'
        verbose_name_plural = 'Заказы, которые доставит курьер'


class Basket(models.Model):
    id_user = models.IntegerField()
    id_food = models.CharField(max_length=123213)

    object = models.Manager()