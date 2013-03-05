import os
from datetime import datetime
from django.conf import settings


REDACTOR_API_ROOT_FOLDER = getattr(settings, "REDACTOR_API_ROOT_FOLDER", "redactor_api")


def get_root_path(folder_name=""):
    folder = os.path.join(
        REDACTOR_API_ROOT_FOLDER,
        folder_name,
        datetime.today().strftime('%Y/%m/%d/'))
    path = os.path.join(settings.MEDIA_ROOT, folder)
    if not os.path.exists(path):
        os.makedirs(path)
    return folder, path


def handle_uploaded_file(f, path):
    destination = open(path, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()


def get_image_folders(folder):
    folder = folder[1:] if folder.startswith("/") else folder
    browse_path = os.path.join(settings.MEDIA_ROOT, folder)
    root, dirs, files = os.walk(browse_path).next()
    return dirs


def get_image_files(user=None, folder=""):
    """
    Recursively walks all dirs under upload dir and generates a list of
    full paths for each file found.
    """
    if user and not user.is_superuser:
        user_path = user.username
    else:
        user_path = ''

    browse_path = os.path.join(settings.MEDIA_ROOT, folder)
    folder = folder[1:] if folder.startswith("/") else folder
    root, dirs, files = os.walk(browse_path).next()
    media_root = settings.MEDIA_URL + folder
    for filename in [os.path.join(media_root, x) for x in files]:
        tokens = filename.split(".")
        ext = tokens[len(tokens) - 1]
        if ext not in ["jpg", "jpeg", "gif", "png", "svg", "ico"]:
            continue
        yield dict(
            thumb=filename,
            image=filename,
            folder=root
        )


def get_file_path(name, root_path):
    clone = ""
    counter = 0
    while os.path.exists(os.path.join(root_path, clone + name)):
        clone = "%s" % counter
        counter += 1
    path = os.path.join(root_path, clone, name)
    return clone + name, path