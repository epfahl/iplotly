"""Define utility functions for the iplotly package.
"""

import os
import yaml
import json
import plotly

DEFAULTS_FILE = "defaults.yml"


# ------------------------------

def local_filepath(file):
    return os.path.join(os.path.dirname(__file__), file)

    os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(file)))


def yaml_load(filepath):
    with open(filepath, "r") as f:
        data = yaml.load(f)
    return data


def load_defaults(file=DEFAULTS_FILE):
    return yaml_load(local_filepath(file))


def fig_show(fig):
    """Show the Plotly figure in a Jupyter notebook.
    """
    return plotly.offline.iplot(fig, show_link=False)


def fig_to_json(fig):
    """Return the JSON serialization of the Plotly figure.
    """
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def fig_to_html(fig, path):
    """Render the Plotly figure and save as HTML at the given path (saved
    locally if path not specified.)
    """
    ext = os.path.splitext(path)[1][1:]
    if ext != 'html':
        raise ValueError("the filename must have an 'html' extension")
    return plotly.offline.plot(
        fig, filename=path, show_link=False, auto_open=False)


def unique_key(typ, name, keys):
    """Generate a unique trace key given the trace type, requested name, and
    list of existing keys.
    """
    if name is not None:
        if name in keys:
            if isinstance(name, int):
                return name + 1
            elif isinstance(name, basestring):
                return name + str(len(keys))
            else:
                raise ValueError(
                    "key '{}' not recognized; must be an integer or string"
                    .format(name))
        else:
            return name
    else:
        return typ + "_" + str(len(keys))


def thread(obj, calls):
    """Given an instance of the chart class and a list of method calls (as
    dicts), return an update of the chart object after applying the method.
    Each element in the call list has the form

    {
        'mth': <str method name>,
        'args': <sequence of method positional args>,
        'kwargs': <dict of method keyword arguments>
    }

    Notes
    -----
    There's nothing specific to Plotly here.  This will work for any class
    whose requested methods return self, allowing them to be chained.

    ToDo
    ----
    Show a usage example.
    """

    def _call(v, c):
        return getattr(v, c['mth'])(
            *c.get('args', []), **c.get('kwargs', {}))

    return reduce(_call, calls, obj)
