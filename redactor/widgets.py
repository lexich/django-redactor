from urlparse import urljoin

from django.conf import settings
from django.core.urlresolvers import reverse
from django.forms import Media, Textarea
from django.utils.safestring import mark_safe
from django.utils import simplejson as json


class RedactorEditor(Textarea):
    """
    A widget that renders a <textarea> element as a Redactor rich tech editor.

    This widget has three additional keyword arguments that a typical ``Textarea``
    wiget does not. They are:

    ``redactor_settings`` - a dictionary of named settings and values. See the
    Redactor `API docs <http://redactorjs.com/docs/settings>`_ for available
    settings. If you provide a string instead of a dictionary, it will be used
    as is.

    ``redactor_css`` - a path to a CSS file to include in the editable content
    region of the widget. Paths used to specify media can be either relative or
    absolute. If a path starts with '/', 'http://' or 'https://', it will be
    interpreted as an absolute path, and left as-is. All other paths will be
    prepended with the value of the ``STATIC_URL`` setting (or ``MEDIA_URL`` if
    static is not defined).

    Example usage::

        >>> RedactorEditor(
                redactor_css = 'styles/bodycopy.css',
                redactor_settings={
                    'lang': 'en',
                    'load': True,
                    'path': False,
                    'focus': False,
                }
            )

        >>> RedactorEditor(
                redactor_settings="{lang: 'en'}"
            )

    """

    script_tag = '<script type="text/javascript">Redactor.register(%s);</script>'

    def __init__(self, attrs=None, redactor_css=None, redactor_settings=None, include_jquery=True):
        super(RedactorEditor, self).__init__(attrs=attrs)
        self.include_jquery = include_jquery
        default_settings = {
            'lang': 'en',
            'load': True,
            'path': False,
            'focus': False,
            'autoresize': True
        }
        if redactor_settings:
            default_settings.update(redactor_settings)
        self.redactor_settings = default_settings
        if redactor_css:
            self.redactor_settings['css'] = self.get_redactor_css_absolute_path(redactor_css)

    def _get_js_media(self):
        js = (
            'django-redactor/redactor/redactor.js',
            'django-redactor/redactor/setup.js',
        )
        if self.include_jquery:
            js = ('redactor/lib/jquery-1.7.min.js',) + js
        return js

    def get_redactor_css_absolute_path(self, path):
        if path.startswith(u'http://') or path.startswith(u'https://') or path.startswith(u'/'):
            return path
        else:
            if settings.STATIC_URL is None:
                prefix = settings.MEDIA_URL
            else:
                prefix = settings.STATIC_URL
            return urljoin(prefix, path)

    @property
    def media(self):
        js = self._get_js_media()
        if self.redactor_settings['lang'] != 'en':
            js += ('django-redactor/redactor/langs/%s.js' % self.redactor_settings['lang'],)
        css = {
            'screen': [
                'redactor/redactor/redactor.css',
            ]
        }
        return Media(css=css, js=js)

    def render(self, name, value, attrs=None):
        html_class_name = attrs.get('class', '')
        redactor_class = html_class_name and " redactor_content" or "redactor_content"
        html_class_name += redactor_class
        attrs['class'] = html_class_name
        html = super(RedactorEditor, self).render(name, value, attrs=attrs)
        if isinstance(self.redactor_settings, basestring):
            html += self.script_tag % self.redactor_settings.replace('\n', '')
        else:
            html += self.script_tag % json.dumps(self.redactor_settings)
        return mark_safe(html)


class AdminRedactorEditor(RedactorEditor):
    @property
    def media(self):
        js = self._get_js_media()
        if self.redactor_settings['lang'] != 'en':
            js += ('django-redactor/redactor/langs/%s.js' % self.redactor_settings['lang'],)
        css = {
            'screen': [
                'redactor/redactor/redactor.css',
                'django-redactor/redactor/css/django_admin.css',
            ]
        }
        return Media(css=css, js=js)


class AdminRedactorEditorEx(AdminRedactorEditor):
    """
    Customize AdminRedactorEditor
    """

    def __init__(self, attrs=None, redactor_css=None, redactor_settings=None, include_jquery=True):
        REDACTOR_IMAGE_UPLOAD = getattr(settings, "REDACTOR_IMAGE_UPLOAD", reverse('redactor-upload-image'))
        REDACTOR_FILE_UPLOAD = getattr(settings, "REDACTOR_FILE_UPLOAD", reverse('redactor-upload-file'))
        REDACTOR_IMAGE_GET_JSON = getattr(settings, "REDACTOR_IMAGE_GET_JSON", reverse('redactor-get-json'))
        REDACTOR_LANG = getattr(settings, "REDACTOR_LANG", "ru")
        params_settings = dict(
            imageUpload=REDACTOR_IMAGE_UPLOAD,
            fileUpload=REDACTOR_FILE_UPLOAD,
            imageGetJson=REDACTOR_IMAGE_GET_JSON,
            lang=REDACTOR_LANG
        )
        if redactor_settings:
            params_settings.update(redactor_settings)
        super(AdminRedactorEditorEx, self).__init__(attrs, redactor_css, params_settings, include_jquery)

    @property
    def media(self):
        REDACTOR_CSS = getattr(settings, "REDACTOR_CSS",None)
        media = super(AdminRedactorEditorEx, self).media
        media._js = map(
            lambda x: x if not 'redactor.min.js' else x.replace("redactor.min.js", "redactor.js"), media._js)
        if REDACTOR_CSS:
            media._css["screen"].append(REDACTOR_CSS)
        print(media)
        return media