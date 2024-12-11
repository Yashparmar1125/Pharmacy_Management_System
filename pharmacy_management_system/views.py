from django.shortcuts import render


def LOGIN(request):
    return render(request, 'login.html')