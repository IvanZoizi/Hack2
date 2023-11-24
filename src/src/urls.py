"""
URL configuration for src project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from main.views import main_view
from reg.views import RegisterView, sign_in, logout_user
from src import settings
from buy.views import buy_first_dish, buy_second_dish, buy_third_dish, buy_fours_dish, buy_fives_dish, confirm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_view, name='main_page'),
    path('register/user/', RegisterView.as_view(), name='reg-user'),
    path('login/', sign_in, name='login'),
    path('logout/', logout_user),
    path('buy/1/', buy_first_dish),
    path('buy/2/<int:pk>', buy_second_dish),
    path('buy/3/<int:pk>', buy_third_dish),
    path('buy/4/<int:pk>', buy_fours_dish),
    path('buy/5/<int:pk>', buy_fives_dish),
    path('confirm/<int:pk>', confirm)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
