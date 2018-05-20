from django import views
from django.http import HttpResponse
from django.shortcuts import render


class IndexView(views.View):
    template = 'index.html'

    def get(self, request):
        context = {}
        return render(request, 'index.html', context)


class PostView(views.View):
    template = ''

    def get(self, request, slug):
        return HttpResponse(f'hi: {slug}')
