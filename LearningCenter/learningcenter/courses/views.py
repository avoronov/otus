from django.http import HttpResponse
from django.shortcuts import render


def index_view(request):
    # return HttpResponse('<h1>Hello, World!</h1>')
    return render(request, 'courses/index.html')
