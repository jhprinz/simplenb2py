import os
import os.path

from traitlets.config import Config
from nbconvert.exporters.html import HTMLExporter

# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------


def keep_only_headlines(value, level=5):

    headline_form = [
            '\n\n# =============================================================================\n' + \
            '# {upper}\n' + \
            '# =============================================================================\n' + \
            'print """{upper}"""',

            '\n# {text}',

            '\n\n# -----------------------------------------------------------------------------\n' + \
            '# {text}\n' + \
            '# -----------------------------------------------------------------------------\n' + \
            'print """{text}"""\n',

            '\nprint """# {text}"""',

            '\nprint """## {text}"""',

            '\nprint """### {text}"""',

    ]

    lines = []

    for v in value.split('\n'):
        h_level = len(v.split(' ')[0])
        h_level = h_level if v.split(' ')[0] == '#' * h_level else 0

        full = v.strip()
        text = full[h_level + 1:]

        if h_level > 0 and h_level <= level:
            if len(headline_form[h_level - 1]) > 0:
                lines.append(
                    headline_form[h_level - 1].format(
                        upper=text.upper(),
                        full=full,
                        text=text
                    ))

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
        return '.py'

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
