from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import FormView, CreateView
from .forms import RegisterCompany, RegisterUser, LoginUser
from utils import DataMixin
from dbase.models import User
from uuid import uuid4



def sign_in(request):
    if request.method == 'GET':
        form = LoginUser()
        return render(request, 'register/login_user.html', {'form': form})
    elif request.method == 'POST':
        form = LoginUser(request.POST)

        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            print(phone, password)
            user = User.objects.get(phone=phone)
            if user.check_password(password):
                login(request, user)
                return redirect('main_page')

        # form is not valid or user is not authenticated
        messages.error(request, f'Ошибка, проверьте данные')
        return render(request, 'register/login_user.html', {'form': form})


"""class RegisterView(DataMixin, CreateView):
    template_name = 'register/register_company.html'
    model = User
    form_class = RegisterUser

    def get_success_url(self):
        return reverse('login')

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        data = self.get_user_context()
        return dict(list(content.items()) + list(data.items()))

    def form_valid(self, form):
        data = form.cleaned_data
        user = User.objects.create_user(name=data['name'], phone=data['phone'])
        user.set_password(data['password'])
        user.save()"""


class RegisterView(DataMixin, FormView):
    template_name = 'register/register_user.html'  # добавить файл
    form_class = RegisterUser

    def get_success_url(self):
        return reverse('login')

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        data = self.get_user_context()
        return dict(list(content.items()) + list(data.items()))

    def form_valid(self, form):
        data = form.cleaned_data
        user = User.objects.create_user(name=data['name'], phone=data['phone'], password=data['password'])
        print(user)
        #authenticate(phone=data['phone'], password=data['password'])
        print('Ломается здесь')
        return redirect('login')


def logout_user(request):
    logout(request)
    return redirect('main_page')