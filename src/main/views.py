from django.shortcuts import render


def main_view(request):
    return render(request, 'main/index.html', {'url': '/register/user'})


def main_view_2(request):
    return render(request, 'main/index.html')