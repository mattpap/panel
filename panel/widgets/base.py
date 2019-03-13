"""
Defines the Widget base class which provides bi-directional
communication between the rendered dashboard and the Widget
parameters.
"""
from __future__ import absolute_import, division, unicode_literals

import param

from ..viewable import Reactive


class Widget(Reactive):
    """
    Widgets allow syncing changes in bokeh widget models with the
    parameters on the Widget instance.
    """

    disabled = param.Boolean(default=False, doc="""
       Whether the widget is disabled.""")

    name = param.String(default='')

    height = param.Integer(default=None, bounds=(0, None))

    width = param.Integer(default=None, bounds=(0, None))

    __abstract = True

    _widget_type = None

    _supports_embed = False

    _rename = {'name': 'title'}

    def __init__(self, **params):
        if 'name' not in params:
            params['name'] = ''
        super(Widget, self).__init__(**params)

    def _get_model(self, doc, root=None, parent=None, comm=None):
        model = self._widget_type(**self._process_param_change(self._init_properties()))
        if root is None:
            root = model
        # Link parameters and bokeh model
        values = dict(self.get_param_values())
        properties = list(self._process_param_change(values))
        self._models[root.ref['id']] = (model, parent)
        self._link_props(model, properties, doc, root, comm)
        return model

    def _get_embed_state(self, root, parent, max_opts=3):
        """
        Returns the bokeh model and a discrete set of value states
        for the widget.

        Arguments
        ---------
        root: bokeh.model.Model
          The root model of the widget
        parent: bokeh.model.Model
          The parent model of the widget
        max_opts: int
          The maximum number of states the widget should return

        Returns
        -------
        widget: panel.widget.Widget
          The Panel widget instance to modify to effect state changes
        model: bokeh.model.Model
          The bokeh model to record the current value state on
        values: list
          A list of value states to explore.
        """


class CompositeWidget(Widget):
    """
    A baseclass for widgets which are made up of two or more other
    widgets
    """

    __abstract = True

    def select(self, selector=None):
        """
        Iterates over the Viewable and any potential children in the
        applying the Selector.

        Arguments
        ---------
        selector: type or callable or None
            The selector allows selecting a subset of Viewables by
            declaring a type or callable function to filter by.

        Returns
        -------
        viewables: list(Viewable)
        """
        objects = super(CompositeWidget, self).select(selector)
        for obj in self._composite.objects:
            objects += obj.select(selector)
        return objects
