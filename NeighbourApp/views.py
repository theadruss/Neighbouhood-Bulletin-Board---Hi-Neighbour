from django.shortcuts import render

def index(request):
    return render(request, 'index.html')


def signup(request):
    return render(request, 'signup.html')

def local(request):
    return render(request, 'local.html')

def group(request):
    return render (request, 'group.html')
