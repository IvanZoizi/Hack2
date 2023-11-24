from django.shortcuts import render
from dbase.models import Food, Basket
from forms import Delivery


def buy_first_dish(request):

    all_food = Food.objects.all()
    data = []
    for i in all_food:
        if i.count > 0 and i.type_food == 'Первое блюдо':
            data.append(i)
    return render(request, 'buy/buy.html', {'elems': data})


def buy_second_dish(request, pk):
    user = request.user
    basket = Basket.object.get(id_user=user.id)
    if basket:
        basket.delete()
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
            if elem != '0':
                food = Food.objects.get(id_food=int(elem))
                food.count -= 1
                result += food.price
                check_list.append(food.title)
        if result == 0:
            return render(request, 'buy/confirm.html', {'error': 'Вы не выбрали ни одного блюда'})
        else:
            return render(request, 'buy/confirm.html', {'price': result, 'check_list': check_list, 'form': form})
    elif request.method == 'POST':
        form = Delivery(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)