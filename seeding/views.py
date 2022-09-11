from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render


def index(request):
    return HttpResponse('Тестовое представление')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
