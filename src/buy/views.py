import datetime

from django.shortcuts import render, redirect
from dbase.models import Food, Basket, Statistics, NewOrders, Business
from .forms import Delivery


def buy_first_dish(request):

    all_food = Food.objects.all()
    data = []
    for i in all_food:
        if i.count > 0 and i.type_food == 'Первое блюдо':
            data.append(i)
    return render(request, 'buy/buy.html', {'elems': data})


def buy_second_dish(request, pk):
    user = request.user
    try:
        basket = Basket.object.get(id_user=user.id)
        if basket:
            basket.delete()
    except Exception as ex:
        pass
    order = Basket(id_user=user.id)
    if pk != 0:
        first_food = Food.objects.get(id_food=pk)
        order.id_food = str(first_food.id_food) + ','
    else:
        order.id_food = '0,'
    order.save()
    all_food = Food.objects.all()
    data = []
    for i in all_food:
        if i.count > 0 and i.type_food == 'Второе блюдо':
            data.append(i)
    return render(request, 'buy/buy2.html', {'elems': data})


def buy_third_dish(request, pk):
    user = request.user
    order = Basket.object.get(id_user=user.id)
    if pk != 0:
        first_food = Food.objects.get(id_food=pk)
        order.id_food = order.id_food + str(first_food.id_food) + ','
    else:
        order.id_food = order.id_food + '0,'
    order.save()
    all_food = Food.objects.all()
    print(all_food)
    data = []
    for i in all_food:
        if i.count > 0 and i.type_food == 'Салаты':
            data.append(i)
    return render(request, 'buy/buy3.html', {'elems': data})


def buy_fours_dish(request, pk):
    user = request.user
    order = Basket.object.get(id_user=user.id)
    if pk != 0:
        first_food = Food.objects.get(id_food=pk)
        order.id_food = order.id_food + str(first_food.id_food) + ','
    else:
        order.id_food = order.id_food + '0,'
    order.save()
    all_food = Food.objects.all()
    print(all_food)
    data = []
    for i in all_food:
        if i.count > 0 and i.type_food == 'Десерты':
            data.append(i)
    return render(request, 'buy/buy4.html', {'elems': data})


def buy_fives_dish(request, pk):
    user = request.user
    order = Basket.object.get(id_user=user.id)
    if pk != 0:
        first_food = Food.objects.get(id_food=pk)
        order.id_food = order.id_food + str(first_food.id_food) + ','
    else:
        order.id_food = order.id_food + '0,'
    order.save()
    all_food = Food.objects.all()
    data = []
    for i in all_food:
        if i.count > 0 and i.type_food == 'Напиток':
            data.append(i)
    return render(request, 'buy/buy5.html', {'elems': data})


def confirm(request, pk):
    if request.method == 'GET':
        form = Delivery()
        user = request.user
        order = Basket.object.get(id_user=user.id)
        if pk != 0:
            first_food = Food.objects.get(id_food=pk)
            order.id_food = order.id_food + str(first_food.id_food) + ','
        else:
            order.id_food = order.id_food + '0,'
        order.save()
        result = 0
        check_list = []
        for elem in order.id_food.split(','):
            print(elem)
            if elem != '0' and elem != '':
                food = Food.objects.get(id_food=int(elem))
                result += food.price
                check_list.append(food.title)
        if result == 0:
            return render(request, 'buy/confirm.html', {'error': 'Вы не выбрали ни одного блюда'})
        else:
            return render(request, 'buy/confirm.html', {'price': result, 'check_list': ','.join(check_list), 'form': form})
    elif request.method == 'POST':
        form = Delivery(request.POST)
        if form.is_valid():
            print(1231232)
            result = 0
            check_list = []
            data = form.cleaned_data
            user = request.user
            basket = Basket.object.get(id_user=user.id)
            for elem in basket.id_food.split(','):
                if elem != '0' and elem != '':
                    food = Food.objects.get(id_food=int(elem))
                    food.count -= 1
                    food.save()
                    result += food.price
                    check_list.append(food.title)
                    try:
                        static = Statistics.object.get(food_name=food.title, day_of_the_week=datetime.datetime.now().strftime('%A'),
                                                       date=datetime.datetime.now().strftime("%d.%m.%Y"))
                        static.count += 1
                        static.price += food.price
                        static.remained = food.count
                    except Exception:
                        static = Statistics(food_name=food.title, day_of_the_week=datetime.datetime.now().strftime('%A'),
                                                       date=datetime.datetime.now().strftime("%d.%m.%Y"))
                        static.count = 1
                        static.price = food.price
                        static.remained = food.count
                    static.save()
            new_order = NewOrders(user_name=user.name, user_phone=user.phone, price=result, foods=','.join(check_list),
                                  delivery='Да' if data['check'] else 'Нет', floor=data['floor'] if data['check'] else '')
            new_order.save()
            return redirect('/success')


def success(request):
    return render(request, 'buy/success.html')


def business(request):
    all_b = Business.object.all()
    data = []
    for i in all_b:
        if i.count > 0:
            data.append(i)
    return render(request, 'buy/business.html', {"elems": data})


def buy_business(request, pk):
    if request.method == 'GET':
        form = Delivery()
        lanch = Business.object.get(id=pk)
        return render(request, 'buy/confirm.html', {'price': lanch.price, 'check_list': lanch.title, 'form': form})
    else:
        user = request.user
        form = Delivery(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            food = Business.object.get(id=pk)
            food.count -= 1
            food.save()
            try:
                static = Statistics.object.get(food_name=food.title,
                                               day_of_the_week=datetime.datetime.now().strftime('%A'),
                                               date=datetime.datetime.now().strftime("%d.%m.%Y"))
                static.count += 1
                static.price += food.price
                static.remained = food.count
            except Exception:
                static = Statistics(food_name=food.title, day_of_the_week=datetime.datetime.now().strftime('%A'),
                                    date=datetime.datetime.now().strftime("%d.%m.%Y"))
                static.count = 1
                static.price = food.price
                static.remained = food.count
            static.save()

            new_order = NewOrders(user_name=user.name, user_phone=user.phone, price=food.price, foods=f'Бизнес ланч - {food.title}',
                                  delivery='Да' if data['check'] else 'Нет', floor=data['floor'] if data['check'] else '')
            new_order.save()
            return redirect('/success')