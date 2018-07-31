from django import views
from django.http import HttpResponse
from django.shortcuts import render
from . import models


class IndexView(views.View):
    template = 'index.html'

    def get(self, request):
        # todo: pagination
        posts = models.Post.objects.all()
        context = {
            'posts': posts
        }
        return render(request, 'index.html', context)


class PostView(views.View):
    template = ''

    def get(self, request, slug):
        return HttpResponse(f'hi: {slug}')
