from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.urls import reverse


class UserAccountManager(BaseUserManager):
    def create_user(self, phone, password):
        if not phone:
            raise ValueError('Email must be set!')
        user = self.model(phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password):
        user = self.create_user(phone, password)
        user.is_staff = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email_):
        return self.get()


class Restaurant(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=120, verbose_name='Название ресторана', help_text='Введите название ресторана')
    description = models.CharField(max_length=300, verbose_name='Описание', help_text='Введите описание ресторана')
    address = models.CharField(max_length=120, verbose_name='Адрес', help_text='Введите адрес ресторана')

    def get_absolute_url(self):
        return reverse('restaurant', args=[self.title])

    def __str__(self):
        return self.title


class Food(models.Model):
    id_food = models.IntegerField(primary_key=True)
    photo = models.ImageField(verbose_name='Фотография блюда')
    title = models.CharField(max_length=120, verbose_name='Название блюда', help_text='Введите название блюда')
    price = models.IntegerField()
    structure = models.CharField(max_length=300, verbose_name='Состав', help_text='Напишите из чего состоит блюдо')

    id_restaurant = models.ManyToManyField(Restaurant)

    def get_absolute_url(self):
        return reverse('food', args=[self.id_food])

    def __str__(self):
        return self.title


class Company(models.Model):
    company_token = models.CharField(max_length=500, verbose_name='Токен для подключения сотрудников')
    title = models.CharField(max_length=120, verbose_name='Название компании', help_text='Введите название команды')
    adresses = models.CharField(max_length=10000, verbose_name='Адреса компании', help_text='Введите все адреса вашей компании через запятую')
    balance = models.IntegerField(verbose_name='Баланс пользователя', help_text='Введите стоимость заказа пользователя')

    def get_absolute_url(self):
        return reverse('company', args=[str(self.title)])

    def get_token(self):
        return self.company_token

    def __str__(self):
        return self.title


class User(AbstractBaseUser):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=120, verbose_name='Имя, фамилия пользователя пользователя', help_text='Ваше имя и фамилию', unique=True)
    company_token = models.CharField(max_length=500, verbose_name='Токен для подключения сотрудников')
    password = models.CharField(max_length=120, verbose_name='Пароль пользователя', help_text='Введите ваш пароль')
    phone = models.CharField(max_length=120, verbose_name='Номер телефона', help_text='Введите ваш номер телефона', unique=True)
    address = models.CharField(max_length=120, verbose_name='Адрес', help_text='Введите ваш адрес')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()
    company = models.ManyToManyField(Company)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['password']

    class Meta:
        verbose_name = 'Пользователь'
        db_table = 'user'
        ordering = ['phone']

    def __str__(self):
        return self.phone

    def get_absolute_url(self):
        return reverse('user-info', args=[str(self.phone)])

    def get_full_name(self):
        return self.name

    def natural_key(self):
        return self.phone


class Orders(models.Model):
    #id_food = models.IntegerField(verbose_name='Id блюда')
    quantity = models.IntegerField(verbose_name='Кол-во порций')
    comment = models.CharField(max_length=300, verbose_name='Комментарий пользователя')
    id_food = models.ManyToManyField(Food)
    id_user = models.ManyToManyField(User)

    def get_absolute_url(self):
        return reverse('order', args=[self.id_user.name, self.id_food])

    def __str__(self):
        return self.id_user.name