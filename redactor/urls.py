# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views


urlpatterns = patterns(
    '',
    url(r'^uploadimage$',
        views.upload_image,
        name="redactor-upload-image"),

    url(r'^uploadfile$',
        views.upload_file,
        name="redactor-upload-file"),

    url(r'^getjson',
        views.get_json_images,
        name="redactor-get-json"),
)
