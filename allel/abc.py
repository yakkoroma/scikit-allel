# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division


# third-party imports
import numpy as np


class ArrayWrapper(object):
    """Abstract base class that delegates everything to a wrapped array-like object."""

    def __init__(self, values):
        self._values = values

    @property
    def values(self):
        """The underlying array of values."""
        return self._values

    def __getattr__(self, item):
        return getattr(self.values, item)

    def __getitem__(self, item):
        return self.values[item]

    def __setitem__(self, item, value):
        self.values[item] = value

    def __iter__(self):
        return iter(self.values)

    def __len__(self):
        return len(self.values)

    def __array__(self, *args):
        a = np.asarray(self.values)
        if args:
            a = a.astype(args[0])
        return a

    def __str__(self):
        return str(self.values)

    def __repr__(self):
        return repr(self.values)

    def __eq__(self, other):
        return self.values == other

    def __ne__(self, other):
        return self.values != other

    def __lt__(self, other):
        return self.values < other

    def __gt__(self, other):
        return self.values > other

    def __le__(self, other):
        return self.values <= other

    def __ge__(self, other):
        return self.values >= other

    def __abs__(self):
        return abs(self.values)

    def __add__(self, other):
        return self.values + other

    def __and__(self, other):
        return self.values & other

    def __div__(self, other):
        return self.values.__div__(other)

    def __floordiv__(self, other):
        return self.values // other

    def __inv__(self):
        return ~self.values

    def __invert__(self):
        return ~self.values

    def __lshift__(self, other):
        return self.values << other

    def __mod__(self, other):
        return self.values % other

    def __mul__(self, other):
        return self.values * other

    def __neg__(self):
        return -self.values

    def __or__(self, other):
        return self.values | other

    def __pos__(self):
        return +self.values

    def __pow__(self, other):
        return self.values ** other

    def __rshift__(self, other):
        return self.values >> other

    def __sub__(self, other):
        return self.values - other

    def __truediv__(self, other):
        return self.values.__truediv__(other)

    def __xor__(self, other):
        return self.values ^ other


def arr1d_to_html(indices, items, caption):
    # N.B., table captions don't render in jupyter notebooks on GitHub,
    # so put caption outside table element

    # sanitize caption
    caption = caption.replace('<', '&lt;')
    # caption = caption.strip().replace('\n', '<br/>')
    html = caption

    # build table
    html += '<table>'
    html += '<tr>'
    html += ''.join(['<th style="text-align: center">%s</th>' % i
                     for i in indices])
    html += '</tr>'
    html += '<tr>'
    html += ''.join(['<td style="text-align: center">%s</td>' % item
                     for item in items])
    html += '</tr>'
    html += '</table>'

    return html


def arr2d_to_html(row_indices, col_indices, items, caption):
    # N.B., table captions don't render in jupyter notebooks on GitHub,
    # so put caption outside table element

    # sanitize caption
    caption = caption.replace('<', '&lt;')
    # caption = caption.strip().replace('\n', '<br/>')
    html = caption

    # build table
    html += '<table>'
    html += '<tr><th></th>'
    html += ''.join(['<th style="text-align: center">%s</th>' % i
                     for i in col_indices])
    html += '</tr>'
    for row_index, row in zip(row_indices, items):
        if row_index == ' ... ':
            html += '<tr><th style="text-align: center">...</th>' \
                    '<td style="text-align: center" colspan=%s>...</td></tr>' % \
                    (len(col_indices) + 1)
        else:
            html += '<tr><th style="text-align: center">%s</th>' % row_index
            html += ''.join(['<td style="text-align: center">%s</td>' % item
                             for item in row])
            html += '</tr>'
    html += '</table>'

    return html


def recarr_to_html(names, indices, items, caption):
    # N.B., table captions don't render in jupyter notebooks on GitHub,
    # so put caption outside table element

    # sanitize caption
    caption = caption.replace('<', '&lt;')
    # caption = caption.strip().replace('\n', '<br/>')
    html = caption

    # build table
    html += '<table>'
    html += '<tr><th></th>'
    html += ''.join(['<th style="text-align: center">%s</th>' % n
                     for n in names])
    html += '</tr>'
    for row_index, row in zip(indices, items):
        if row_index == ' ... ':
            html += '<tr><th style="text-align: center">...</th>' \
                    '<td style="text-align: center" colspan=%s>...</td></tr>' % \
                    (len(names) + 1)
        else:
            html += '<tr><th style="text-align: center">%s</th>' % row_index
            html += ''.join(['<td style="text-align: center">%s</td>' % item
                             for item in row])
            html += '</tr>'
    html += '</table>'

    return html


class Displayable(ArrayWrapper):

    @property
    def caption(self):
        return '%s(%s, dtype=%s)\n' % (type(self).__name__, self.shape, self.dtype)

    def __repr__(self):
        return self.caption + '\n' + str(self)

    def __str__(self):
        return self.to_display_str()

    def _repr_html_(self):
        return self.to_display_html()

    def to_str_items(self):
        raise NotImplementedError


# noinspection PyAbstractClass
class Displayable1D(Displayable):

    def get_display_items(self, threshold, edgeitems):

        # ensure threshold
        if threshold is None:
            threshold = self.shape[0]

        # ensure sensible edgeitems
        edgeitems = min(edgeitems, threshold // 2)

        # determine indices of items to show
        if self.shape[0] > threshold:
            indices = (
                list(range(edgeitems)) + [' ... '] +
                list(range(self.shape[0] - edgeitems, self.shape[0], 1))
            )
            head = self[:edgeitems].to_str_items()
            tail = self[-edgeitems:].to_str_items()
            items = head + [' ... '] + tail
        else:
            indices = list(range(self.shape[0]))
            items = self[:].to_str_items()

        return indices, items

    def to_display_str(self, threshold=10, edgeitems=5):
        _, items = self.get_display_items(threshold, edgeitems)
        s = ' '.join(items)
        return s

    def to_display_html(self, threshold=10, edgeitems=5, caption=None):
        indices, items = self.get_display_items(threshold, edgeitems)
        if caption is None:
            caption = self.caption
        return arr1d_to_html(indices, items, caption)

    def display(self, threshold=10, edgeitems=5, caption=None):
        html = self.to_display_html(threshold, edgeitems, caption)
        from IPython.display import display_html
        display_html(html, raw=True)

    def displayall(self, caption=None):
        self.display(threshold=None, caption=caption)


# noinspection PyAbstractClass
class Displayable2D(Displayable):

    def get_display_items(self, row_threshold, col_threshold, row_edgeitems,
                          col_edgeitems):

        # ensure threshold
        if row_threshold is None:
            row_threshold = self.shape[0]
        if col_threshold is None:
            col_threshold = self.shape[1]

        # ensure sensible edgeitems
        row_edgeitems = min(row_edgeitems, row_threshold // 2)
        col_edgeitems = min(col_edgeitems, col_threshold // 2)

        # determine row indices of items to show
        if self.shape[0] > row_threshold:
            row_indices = (
                list(range(row_edgeitems)) + [' ... '] +
                list(range(self.shape[0] - row_edgeitems, self.shape[0], 1))
            )
            head = self[:row_edgeitems].to_str_items()
            tail = self[-row_edgeitems:].to_str_items()
            items = head + [' ... '] + tail
        else:
            row_indices = list(range(self.shape[0]))
            items = self[:].to_str_items()

        # determine col indices of items to show
        if self.shape[1] > col_threshold:
            col_indices = (
                list(range(col_edgeitems)) + [' ... '] +
                list(range(self.shape[1] - col_edgeitems, self.shape[1], 1))
            )
            items = [
                row if row == ' ... ' else
                (row[:col_edgeitems] + [' ... '] + row[-col_edgeitems:])
                for row in items
            ]
        else:
            col_indices = list(range(self.shape[1]))
            # items unchanged

        return row_indices, col_indices, items

    def to_display_str(self, row_threshold=6, col_threshold=10, row_edgeitems=3,
                       col_edgeitems=5):
        _, _, items = self.get_display_items(row_threshold, col_threshold, row_edgeitems,
                                             col_edgeitems)
        s = ''
        for row in items:
            if row == ' ... ':
                s += row + '\n'
            else:
                s += ' '.join(row) + '\n'
        return s

    def to_display_html(self, row_threshold=6, col_threshold=10, row_edgeitems=3,
                        col_edgeitems=5, caption=None):
        row_indices, col_indices, items = self.get_display_items(
            row_threshold, col_threshold, row_edgeitems, col_edgeitems
        )
        if caption is None:
            caption = self.caption
        return arr2d_to_html(row_indices, col_indices, items, caption)

    def display(self, row_threshold=6, col_threshold=10, row_edgeitems=3,
                col_edgeitems=5, caption=None):
        html = self.to_display_html(row_threshold, col_threshold, row_edgeitems,
                                    col_edgeitems, caption)
        from IPython.display import display_html
        display_html(html, raw=True)

    def displayall(self, caption=None):
        self.display(row_threshold=None, col_threshold=None, caption=caption)


class DisplayableTable(Displayable):

    @property
    def names(self):
        """Column names."""
        return self.dtype.names

    def to_str_items(self):
        tmp = self[:]
        items = [[repr(x) for x in row] for row in tmp]
        return items

    def get_display_items(self, threshold, edgeitems):

        # ensure threshold
        if threshold is None:
            threshold = self.shape[0]

        # ensure sensible edgeitems
        edgeitems = min(edgeitems, threshold // 2)

        # determine indices of items to show
        if self.shape[0] > threshold:
            indices = (
                list(range(edgeitems)) + [' ... '] +
                list(range(self.shape[0] - edgeitems, self.shape[0], 1))
            )
            head = self[:edgeitems].to_str_items()
            tail = self[-edgeitems:].to_str_items()
            items = head + [' ... '] + tail
        else:
            indices = list(range(self.shape[0]))
            items = self[:].to_str_items()

        return indices, items

    def to_display_str(self, threshold=10, edgeitems=5):
        _, items = self.get_display_items(threshold, edgeitems)
        s = ' '.join(items)
        return s

    def to_display_html(self, threshold=10, edgeitems=5, caption=None):
        indices, items = self.get_display_items(threshold, edgeitems)
        if caption is None:
            caption = self.caption
        return recarr_to_html(self.names, indices, items, caption)

    def display(self, threshold=10, edgeitems=5, caption=None):
        html = self.to_display_html(threshold, edgeitems, caption)
        from IPython.display import display_html
        display_html(html, raw=True)

    def displayall(self, caption=None):
        self.display(threshold=None, caption=caption)

    def __repr__(self):
        return self.caption + '\n' + str(self)

    def __str__(self):
        return str(self.values)