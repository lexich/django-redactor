import os
from datetime import datetime
from django.conf import settings
from django.http import Http404

REDACTOR_API_ROOT_FOLDER = getattr(settings, "REDACTOR_API_ROOT_FOLDER", "redactor_api")
REDACTOR_IMAGES_EXT = getattr(settings, "REDACTOR_IMAGES_EXT", ["jpg", "jpeg", "gif", "png", "svg", "ico"])
REDACTOR_FILES_EXT = getattr(settings, "REDACTOR_FILES_EXT", ["rtf", "doc", "docx", "xml", "pfd", "odt"])


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
    try:
        root, dirs, files = os.walk(browse_path).next()
    except Exception, e:
        raise Http404()
    return dirs


def get_image_files(folder=""):
    browse_path = os.path.join(settings.MEDIA_ROOT, folder)
    folder = folder[1:] if folder.startswith("/") else folder
    root, dirs, files = os.walk(browse_path).next()
    media_root = settings.MEDIA_URL + folder
    for dir in dirs:
        yield dict(type="dir", folder=dir, folderName=dir)
    for filename in [os.path.join(media_root, x) for x in files]:
        tokens = filename.split(".")
        ext = tokens[len(tokens) - 1]
        if ext not in REDACTOR_IMAGES_EXT:
            continue
        yield dict(
            type="image",
            thumb=filename,
            image=filename,
            folder=media_root
        )


def get_file_path(name, root_path):
    clone = ""
    counter = 0
    while os.path.exists(os.path.join(root_path, clone + name)):
        clone = "%s" % counter
        counter += 1
    path = os.path.join(root_path, clone, name)
    return clone + name, path


def normalize_path(path, root):
    """
    Normalizing path
    :param path: path to file
    :param root: root folder
    :return: normalizing path
    """
    if path.startswith("/") or path == "":
        path = u".%s" % path
    path = os.path.join(root, path)
    return path


def get_abspath_or_404(path, root=settings.MEDIA_ROOT):
    """
    Get absolute path and protection from transversal directory attack
    :param path: path to file
    :param root: root folder
    :return: absolute path
    """
    path = normalize_path(path, root)
    if ".." in os.path.relpath(path, root):
        raise Http404()
    return os.path.abspath(path)


def get_relpath_or_404(path, root=settings.MEDIA_ROOT):
    """
    Get relative path and protection from transversal directory attack
    :param path: path to file
    :param root: root folder
    :return: relative path
    """
    path = normalize_path(path, root)
    relpath = os.path.relpath(path, root)
    if ".." in relpath:
        raise Http404()
    return relpath


