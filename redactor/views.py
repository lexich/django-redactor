import json

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from redactor.forms import ImageUploadForm, FileUploadForm
from redactor.utils import get_image_files, get_image_folders


def json_response(func):
    """
    wrapper for json response
    :param func:
    :return:
    """

    def wrap(request, *args, **kwargs):
        data = json.dumps(func(request, *args, **kwargs))
        return HttpResponse(data, content_type="content_type = 'application/javascript; charset=utf8'")

    return wrap


@csrf_exempt
@json_response
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return dict(filelink=form.get_media_url())
    return {}


@csrf_exempt
@json_response
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return dict(
                filelink=form.get_media_url(),
                filename=form.get_filename()
            )
    return {}


@json_response
def get_json(request):
    root = request.GET.get("folder", "")
    root = root.replace("..", "")
    root = root[1:] if root.startswith("/") else root
    return [meta for meta in get_image_files(request.user, root)]


@json_response
def get_folders(request):
    root = request.GET.get("folder", "")
    root = root.replace("..", "")
    root = root[1:] if root.startswith("/") else root
    return get_image_folders(root)
