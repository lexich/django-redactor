from django import forms
from django.conf import settings
from utils import get_root_path, get_file_path, handle_uploaded_file

__author__ = 'lexich'


class MixinSave(object):
    folder_name = ""
    filename = None
    path = None
    folder = ""

    def save(self):
        self.folder, root_path = get_root_path(self.folder_name)
        name = self.cleaned_data["file"].name
        self.filename, self.path = get_file_path(name, root_path)
        handle_uploaded_file(self.cleaned_data["file"], self.path)

    def get_filename(self):
        return self.filename

    def get_abspath(self):
        return self.path

    def get_media_url(self):
        return settings.MEDIA_URL + self.folder + self.get_filename(),


class ImageUploadForm(MixinSave, forms.Form):
    folder_name = "images"
    file = forms.ImageField()


class FileUploadForm(MixinSave, forms.Form):
    folder_name = "files"
    file = forms.FileField()