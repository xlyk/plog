from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget

from . import models


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ('title', 'body')

    body = forms.CharField(widget=CKEditorWidget())


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'author', 'created_at')

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)
