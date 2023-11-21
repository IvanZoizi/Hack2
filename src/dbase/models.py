from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.urls import reverse
from django.utils.html import format_html
from sorl.thumbnail import get_thumbnail


class UserAccountManager(BaseUserManager):
    def create_user(self, phone, name, password, super=False):
        if not phone:
            raise ValueError('Phone must be set!')
        user = self.model(
            phone=phone,
            name=name
        )
        user.set_password(password)
        if not super:
            user.save(using=self._db)
        return user

    def create_superuser(self, phone, name, password):
        user = self.create_user(
            phone,
            name,
            password=password,
            super=True
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email_):
        return self.get()


class Food(models.Model):
    id_food = models.IntegerField(primary_key=True)
    photo = models.ImageField(verbose_name='Фотография блюда', upload_to='post/photo/%Y/%m/%d/', null=True, blank=True)

    @property
    def thumbnail_preview(self):
        if self.photo:
            _thumbnail = get_thumbnail(self.photo,
                                   '300x300',
                                   upscale=False,
                                   crop=False,
                                   quality=100)
            return format_html('<img src="{}" width="{}" height="{}">'.format(_thumbnail.url, _thumbnail.width, _thumbnail.height))
        return ""

    title = models.CharField(max_length=120, verbose_name='Название блюда', help_text='Введите название блюда')
    price = models.IntegerField(verbose_name='Цена за блюдо', help_text='Введите цену за блюдо')
    structure = models.CharField(max_length=1000, verbose_name='Состав', help_text='Напишите из чего состоит блюдо')
    protein = models.FloatField(verbose_name='Белок', help_text='Укажите сколько содержится белков в блюде в граммах')
    fats = models.FloatField(verbose_name='Жиры', help_text='Укажите сколько содержится жиров в блюде в граммах')
    carbohydrates = models.FloatField(verbose_name='Углеводы',
                                        help_text='Укажите сколько содержится углеводов в блюде')

    objects = models.Manager()

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def get_absolute_url(self):
        return reverse('food', args=[self.id_food])

    def __str__(self):
        return self.title


class Company(models.Model):
    company_token = models.CharField(max_length=500, verbose_name='Токен для подключения сотрудников')
    title = models.CharField(max_length=120, verbose_name='Название компании', help_text='Введите название команды')
    adresses = models.CharField(max_length=10000, verbose_name='Адреса компании', help_text='Введите все адреса вашей компании. Каждый адрес вводите на новой строке')
    balance = models.IntegerField(verbose_name='Баланс пользователя', help_text='Введите стоимость заказа пользователя')
    user_id = models.IntegerField()

    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('company', args=[str(self.title)])

    def get_token(self):
        return self.company_token

    def __str__(self):
        return self.title


class User(AbstractBaseUser):
    id = models.IntegerField(primary_key=True)
    phone = models.CharField(max_length=120, verbose_name='Номер телефона', help_text='Введите ваш номер телефона', unique=True)
    name = models.CharField(max_length=120, verbose_name='Имя', help_text='Ваше имя и фамилию')
    company_token = models.CharField(max_length=500, verbose_name='Токен для подключения сотрудников')
    password = models.CharField(max_length=120, verbose_name='Пароль пользователя', help_text='Введите ваш пароль')
    address = models.CharField(max_length=120, verbose_name='Адрес', help_text='Введите ваш адрес')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

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


class Orders(models.Model):
    #id_food = models.IntegerField(verbose_name='Id блюда')
    quantity = models.IntegerField(verbose_name='Кол-во порций')
    comment = models.CharField(max_length=300, verbose_name='Комментарий пользователя')
    id_food = models.ManyToManyField(Food)
    id_user = models.ManyToManyField(User)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Заказы'
        verbose_name_plural = 'Заказы'

    def get_absolute_url(self):
        return reverse('order', args=[self.id_user.name, self.id_food])

    def __str__(self):
        return self.id_user.name


class Courier(models.Model):
    number_phone = models.CharField(verbose_name='Номер телефона', max_length=12)
    username_telegtam = models.CharField(verbose_name='Username курьера в Telegram', max_length=120)

    object = models.Manager()

    def get_absolute_url(self):
        return reverse('courier', args=[self.username_telegtam])

    def __str__(self):
        return self.username_telegtam