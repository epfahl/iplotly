"""Define custom plot objects that resolve to standard Plotly graph objects.
"""

import plotly.graph_objs as go


# ------------------------------

def _mode(basemode, label):
    """Return the trace mode given a base mode and label bool.
    """
    if label:
        return basemode + "+text"
    else:
        return basemode


class Trace(object):

    def __init__(self, x, y, defs, **props):
        self.x = x
        self.y = y
        self.text = props.get('text')
        self.color = props.get('color', defs['global']['color'])
        self.name = props.get('name', '')
        self.hoverinfo = props.get('hoverinfo', 'all')
        self.showlegend = props.get('showlegend', True)

    @property
    def graph_obj(self):
        raise NotImplementedError

    def __repr__(self):
        return self.graph_obj.__repr__()


class Scatter(Trace):
    """Interface to Plotly Scatter object for generating scatter plots.
    """

    def __init__(self, x, y, defs, **props):
        super(Scatter, self).__init__(x, y, defs, **props)
        self.symbol = props.get('symbol', defs['scatter']['symbol'])
        self.size = props.get('size', defs['scatter']['size'])
        self.opacity = props.get('opacity', defs['scatter']['opacity'])
        self.label = props.get('label', False)
        self.textposition = props.get('textposition', 'top')
        self.mode = _mode('markers', self.label)
        self.line_width = props.get(
            'line_width', defs['scatter']['line_width'])
        self.line_color = props.get('line_color', defs['global']['color'])

    @property
    def graph_obj(self):
        return go.Scatter(
            x=self.x, y=self.y,
            text=self.text,
            mode=self.mode,
            marker=dict(
                symbol=self.symbol, size=self.size,
                color=self.color, opacity=self.opacity,
                line=dict(width=self.line_width, color=self.line_color)),
            name=self.name,
            textposition=self.textposition,
            hoverinfo=self.hoverinfo,
            showlegend=self.showlegend)


class Line(Trace):
    """Interface to Plotly Scatter object for creating line plots.
    """

    def __init__(self, x, y, defs, **props):
        super(Line, self).__init__(x, y, defs, **props)
        self.width = props.get('width', defs['line']['width'])
        self.opacity = props.get('opacity', defs['line']['opacity'])
        self.dash = props.get('dash', defs['line']['dash'])
        self.fill = props.get('fill', defs['line']['fill'])
        self.connectgaps = props.get(
            'connectgaps', defs['line']['connectgaps'])

    @property
    def graph_obj(self):
        return go.Scatter(
            x=self.x, y=self.y,
            text=self.text,
            mode='lines',
            opacity=self.opacity,
            line=dict(width=self.width, color=self.color, dash=self.dash),
            name=self.name,
            hoverinfo=self.hoverinfo,
            fill=self.fill,
            showlegend=self.showlegend,
            connectgaps=self.connectgaps)


class Bar(Trace):
    """Interface to Plotly Bar object for creating bar plots.
    """

    def __init__(self, x, y, defs, **props):
        super(Bar, self).__init__(x, y, defs, **props)
        self.gap = props.get('width', defs['bar']['gap'])
        self.opacity = props.get('opacity', defs['bar']['opacity'])

    @property
    def graph_obj(self):
        return go.Bar(
            x=self.x, y=self.y,
            text=self.text,
            opacity=self.opacity,
            marker=dict(color=self.color),
            name=self.name)
