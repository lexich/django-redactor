import json
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from forms import ImageUploadForm, FileUploadForm
from utils import get_image_files, get_image_folders, get_relpath_or_404


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
@login_required
@json_response
def upload_image(request):
    """
    Upload image
    :param request: HTTP request
    :return: json data in python dict
    """
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return dict(filelink=form.get_media_url())
    return {}


@csrf_exempt
@login_required
@json_response
def upload_file(request):
    """
    Upload file
    :param request: HTTP request
    :return: json data in python dict
    """
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return dict(
                filelink=form.get_media_url(),
                filename=form.get_filename()
            )
    return {}


@login_required
@json_response
def get_json_images(request):
    """
    Get list of image in {request.folder} folder
    :param request: HTTP request
    :return: json data in python dict
    """
    root = request.GET.get("folder", "")
    root = root.replace("..", "")
    root = root[1:] if root.startswith("/") else root
    return [meta for meta in get_image_files(root)]