from django.shortcuts import render
from dbase.models import Food


def buy_first_dish(request):
    all_food = Food.objects.get(type_food='Первое блюдо')
    print(all_food)
    data = []
    for i in all_food:
        if i.count > 0:
            data.append(i)
    return render(request, 'buy/buy.html', {'elems': data})