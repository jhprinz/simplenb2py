import os
import os.path

from traitlets.config import Config
from nbconvert.exporters.html import HTMLExporter

# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------


def keep_only_headlines(value, level=5):
    lines = value.split('\n')
    lines = [v.strip() + '\n' for v in lines if v.split(' ')[0] == '#' * len(v.split(' ')[0]) and len(v.split(' ')[0]) <= level]

    if len(lines) > 0:
        return '\n'.join(lines) + '\n'
    else:
        return ''


def remove_ipython_specific(value):
    value = value.strip().replace('\n\n\n', '\n\n')
    lines = value.split('\n')

    lines = [v for v in lines if len(v) == 0 or v[0] not in ['%', '!']]

    if len(lines) > 0:
        return '\n'.join(lines) + '\n'
    else:
        return ''



class MyExporter(HTMLExporter):
    """
    My custom exporter
    """

    def __init__(self, config, **kwargs):
        super(MyExporter, self).__init__(config, **kwargs)
        self.register_filter('keep_only_headlines', keep_only_headlines)
        self.register_filter('remove_ipython_specific', remove_ipython_specific)

    def _file_extension_default(self):
        """
        The new file extension is `.test_ext`
        """
        return '.simple_py'

    @property
    def template_path(self):
        """
        We want to inherit from HTML template, and have template under
        `./templates/` so append it to the search path. (see next section)
        """
        return super(MyExporter, self).template_path + \
               [os.path.join(os.path.dirname(__file__), "templates")]

    def _template_file_default(self):
        """
        We want to use the new template we ship with our library.
        """
        return 'simple'  # full
