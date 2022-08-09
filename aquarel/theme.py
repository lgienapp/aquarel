from typing import Union, Optional, List
from cycler import cycler
import matplotlib as mpl
import warnings
import json
from .transforms import trim, offset


def _wrap_list_arg(arg):
    if arg is None:
        return arg
    if type(arg) == list:
        return arg
    else:
        return [arg]


class Theme:
    # Options for axis drawing
    _axis_options = ["both", "x", "y"]
    # Options for locations
    _location_options = ["left", "right", "bottom", "top", "center"]
    # Options for horizontal alignment
    _horizontal_alignment_options = [
        "center",
        "right",
        "left",
    ]
    # Options for vertical alignment
    _vertical_alignment_options = [
        "center",
        "top",
        "bottom",
        "baseline",
        "center_baseline",
    ]
    # Options for directions
    _direction_options = ["in", "out", "inout"]
    # Options for ticks
    _tick_options = ["major", "minor", "both"]
    # Optiosn for line styles
    _line_style_options = ["-", "--", "-.", ":", ""]
    # Options for font size
    _font_size_options = [
        "xx-small",
        "x-small",
        "small",
        "medium",
        "large",
        "x-large",
        "xx-large",
    ]
    # Options for font family
    _font_family_options = ["serif", "sans-serif", "monospace", "cursive", "fantasy"]
    # Options for font style
    _font_style_options = ["normal", "roman", "italic", "oblique"]
    # Options for font stretch. This is currently not implemented by matplotlib.
    _font_stretch_options = [
        "ultra-condensed",
        "extra-condensed",
        "condensed",
        "semi-condensed",
        "normal",
        "semi-expanded",
        "expanded",
        "extra-expanded",
        "ultra-expanded",
        "wider",
        "narrower",
    ]
    # Options for font variants.
    _font_variant_options = ["normal", "small-caps"]
    # Options for font weights
    _font_weight_options = [
        "ultralight",
        "light",
        "normal",
        "regular",
        "book",
        "medium",
        "roman",
        "semibold",
        "demibold",
        "demi",
        "bold",
        "heavy",
        "extra bold",
        "black",
    ]
    # Mapping from aquarely keys to transform functions
    _transform_mapping = {"trim": trim, "offset": offset}
    # Mapping from aquarel keys to matplotlib rcparams
    _rcparams_mapping = {
        "title": {
            "location": "axes.titlelocation",
            "pad": "axes.titlepad",
            "size": "axes.titlesize",
            "weight": "axes.titleweight",
        },
        "grid": {
            "draw": ["polaraxes.grid", "axes.grid", "axes3d.grid"],
            "axis": "axes.grid.axis",
            "ticks": "axes.grid.which",
            "alpha": "grid.alpha",
            "style": "grid.linestyle",
            "width": "grid.linewidth",
        },
        "lines": {"style": "lines.linestyle", "width": "lines.linewidth"},
        "fonts": {
            "family": "font.family",
            "cursive": "font.cursive",
            "fantasy": "font.fantasy",
            "monospace": "font.monospace",
            "sans-serif": "font.sans-serif",
            "serif": "font.serif",
            "size": "font.size",
            "stretch": "font.stretch",
            "style": "font.style",
            "variant": "font.variant",
            "weight": "font.weight",
        },
        "colors": {
            "figure_background_color": "figure.facecolor",
            "plot_background_color": "axes.facecolor",
            "axes_color": ["axes.edgecolor", "figure.edgecolor"],
            "line_color": "lines.color",
            "text_color": ["text.color", "axes.titlecolor", "axes.labelcolor"],
            "grid_color": "grid.color",
            "tick_color": ["xtick.color", "ytick.color"],
            "tick_label_color": ["xtick.labelcolor", "ytick.labelcolor"],
            "axis_label_color": "axes.labelcolor",
            "palette": "axes.prop_cycle",
        },
        "axes": {
            "width": "axes.linewidth",
            "bottom": "axes.spines.bottom",
            "left": "axes.spines.left",
            "right": "axes.spines.right",
            "top": "axes.spines.top",
            "xmargin": "axes.xmargin",
            "ymargin": "axes.ymargin",
            "zmargin": "axes.zmargin",
        },
        "ticks": {
            "x_align": "xtick.alignment",
            "y_align:": "ytick.alignment",
            "direction": ["xtick.direction", "ytick.direction"],
            "draw_minor": ["xtick.minor.visible", "ytick.minor.visible"],
            "width_minor": ["xtick.minor.width", "ytick.minor.width"],
            "width_major": ["xtick.major.width", "ytick.major.width"],
            "size_minor": ["xtick.minor.size", "ytick.minor.size"],
            "size_major": ["xtick.major.size", "ytick.major.size"],
            "pad_major": ["xtick.major.pad", "ytick.major.pad"],
            "pad_minor": ["xtick.minor.pad", "ytick.minor.pad"],
        },
        "axis_labels": {
            "pad": "axes.labelpad",
            "size": "axes.labelsize",
            "weight": "axes.labelweight",
        },
        "tick_labels": {
            "location": ["xaxis.labellocation", "yaxis.labellocation"],
            "size": ["xtick.labelsize", "ytick.labelsize"],
            "bottom": "xtick.labelbottom",
            "top": "xtick.labeltop",
            "left": "ytick.labelleft",
            "right": "ytick.labelright",
        },
    }

    def __init__(self, name: Optional[str] = None, description: Optional[str] = None):
        self.info = {}
        if name is not None:
            self.info["name"] = name
        else:
            self.info["name"] = "Untitled"
        if description is not None:
            self.info["description"] = description
        else:
            self.info["description"] = "No description available."
        self.params = {}
        self.overrides = {}
        self.transforms = {}

    def __str__(self):
        return json.dumps(
            {
                "info": self.info,
                "params": self.params,
                "overrides": self.overrides,
                "transforms": self.transforms,
            },
            indent=4,
        )

    def __enter__(self):
        # Save current state
        self.rcparams_orig = mpl.rcParams
        # Apply desired state
        self.apply()

    def __exit__(self, exc_type, exc_val, exc_tb):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", mpl.cbook.MatplotlibDeprecationWarning)
            mpl.rcParams.update(self.rcparams_orig)
        self.apply_transforms()

    def _update_params(self, param_key, value_dict):
        """
        Updates the parameters of the theme.
        :param param_key: the parameter key to modify
        :param value_dict: the value dict to update the parameter key with
        """
        # Filter unset attributes and attributes not in the base style template
        value_dict = dict(
            filter(
                lambda x: (x[0] in self._rcparams_mapping[param_key].keys())
                and (x[1] is not None),
                value_dict.items(),
            )
        )
        # Overwrite parameters with supplied values
        if param_key in self.params.keys():
            # Update existing options if already specified
            self.params[param_key].update(value_dict)
        else:
            # Add new options if previously unspecified
            self.params[param_key] = value_dict

    def _update_transforms(self, value_dict):
        # Filter unset attributes and attributes not in the base transform template
        transforms = dict(
            filter(
                lambda x: (x[0] in self._transform_mapping.keys())
                and (x[1] is not None),
                value_dict.items(),
            )
        )
        self.transforms = transforms

    def save(self, path: str):
        """
        Write the template to a template file
        :param path: file to write the template to
        """
        with open(path, "w") as f:
            json.dump(
                {
                    "info": self.info,
                    "params": self.params,
                    "overrides": self.overrides,
                    "transforms": self.transforms,
                },
                f,
                indent=4,
            )

    def apply(self):
        """
        Applies the theme
        """
        # Clear current state
        mpl.rcParams.update(mpl.rcParamsDefault)
        # Apply desired state
        for top_key in self.params.keys():
            for key, value in self.params[top_key].items():
                mapped_key = self._rcparams_mapping[top_key][key]
                if type(mapped_key) == list:
                    for sub_key in mapped_key:
                        # Special treatment for color palette, as this is otherwise not JSON serializable
                        if mapped_key == "axes.prop_cycle":
                            value = cycler("color", value)
                        mpl.rcParams.update({sub_key: value})
                else:
                    # Special treatment for color palette, as this is otherwise not JSON serializable
                    if mapped_key == "axes.prop_cycle":
                        value = cycler("color", value)
                    mpl.rcParams.update({mapped_key: value})
        if self.overrides is not None:
            mpl.rcParams.update(self.overrides)

    def apply_transforms(self):
        for transform, args in self.transforms.items():
            self._transform_mapping[transform](**args)

    def set_transforms(self, trim: Optional[bool] = None, offset: Optional[int] = None):
        self._update_transforms(
            {
                "trim": {} if trim else None,
                "offset": {"distance": offset} if offset is not None else None,
            }
        )
        return self

    def set_overrides(self, rc: dict):
        """
        Set custom overrides of rcparam parameters directly
        :param rc: Dict of valid matplotlib rcparams
        :return: self
        """
        self.overrides = rc
        return self

    def set_title(
        self,
        location: Optional[str] = None,
        size: Optional[Union[float, str]] = None,
        weight: Optional[Union[float, int, str]] = None,
        pad: Optional[float] = None,
    ):
        """
        Sets title styling options.
        :param location: the location of the title, one of {left, right, center} default: 'center'
        :param pad: pad between axes and title in pt, default: 6.0
        :param size: the font size of the title, float or one of {'xx-small', 'x-small', 'small', 'medium', 'large',
            'x-large', 'xx-large'}, default: 'large'
        :param weight: the font weight of the title, int in range 0-1000 or one of {'ultralight', 'light', 'normal',
            'regular', 'book', 'medium', 'roman', 'semibold', 'demibold', 'demi', 'bold', 'heavy', 'extra bold',
            'black'}, default: "normal"
        :return: self
        """
        self._update_params(
            "title",
            {
                "location": location if location in self._location_options else None,
                "pad": pad,
                "size": size
                if (size in self._font_size_options or type(size) == float)
                else None,
                "weight": weight if weight in self._font_weight_options else None,
            },
        )
        return self

    def set_grid(
        self,
        draw: Optional[bool] = None,
        axis: Optional[str] = None,
        ticks: Optional[str] = None,
        alpha: Optional[float] = None,
        style: Optional[str] = None,
        width: Optional[float] = None,
    ):
        """
        Set grid styling options.
        :param draw: True if grid should be drawn, False otherwise, default: False
        :param axis: axes along which the grid should be drawn, can be "", default: "both"
        :param ticks: which tick level to base the grid on, can be "", default: "major"
        :param alpha: the alpha level to draw the grid with, default: 1.0
        :param style: the line style to draw the grid with, default: "-"
        :param width: the line width to draw the grid with in pt, default: 0.8
        :return: self
        """
        self._update_params(
            "grid",
            {
                "draw": draw,
                "axis": axis if axis in self._axis_options else None,
                "ticks": ticks if ticks in self._tick_options else None,
                "alpha": alpha,
                "style": style if style in self._line_style_options else None,
                "width": width,
            },
        )
        return self

    def set_axes(
        self,
        width: Optional[Union[float, int]] = None,
        top: Optional[bool] = None,
        bottom: Optional[bool] = None,
        left: Optional[bool] = None,
        right: Optional[bool] = None,
        xmargin: Optional[float] = None,
        ymargin: Optional[float] = None,
        zmargin: Optional[float] = None,
    ):
        """
        Set axis styling options
        :param width: edge line width
        :param top: display top axis
        :param bottom: display bottom axis
        :param left: display left axis
        :param right: dislpay right axis
        :param xmargin: padding added to the x-axis, expressed as margin times the data interval
        :param ymargin: padding added to the y-axis, expressed as margin times the data interval
        :param zmargin: padding added to the z-axis, expressed as margin times the data interval
        :return:
        """
        self._update_params(
            "axes",
            {
                "width": width,
                "bottom": bottom,
                "top": top,
                "left": left,
                "right": right,
                "xmargin": xmargin,
                "ymargin": ymargin,
                "zmargin": zmargin,
            },
        )
        return self

    def set_color(
        self,
        palette: Optional[List[str]] = None,
        figure_background_color: Optional[str] = None,
        plot_background_color: Optional[str] = None,
        text_color: Optional[str] = None,
        axes_color: Optional[str] = None,
        axes_label_color: Optional[str] = None,
        line_color: Optional[str] = None,
        grid_color: Optional[str] = None,
        tick_color: Optional[str] = None,
        tick_label_color: Optional[str] = None,
    ):
        """

        :param palette: The color palette to cycle through for plot elements
        :param figure_background_color: the background color of the whole figure
        :param plot_background_color: the background color of the plot only
        :param text_color: color of text elements (plot title, axis title)
        :param axes_color: the color of the axis lines
        :param axes_label_color: the color of the axis labels
        :param line_color: the line color
        :param grid_color: the color of the grid lines
        :param tick_color: the color of the ticks
        :param tick_label_color: the color of the tick labels
        :return: self
        """
        self._update_params(
            "colors",
            {
                "figure_background_color": figure_background_color,
                "plot_background_color": plot_background_color,
                "text_color": text_color,
                "axes_color": axes_color,
                "line_color": line_color,
                "grid_color": grid_color,
                "tick_color": tick_color,
                "tick_label_color": tick_label_color,
                "axes_label_color": axes_label_color,
                "palette": palette,
            },
        )
        return self

    def set_axis_labels(
        self,
        pad: Optional[Union[float, int]] = None,
        size: Optional[str] = None,
        weight: Optional[str] = None,
    ):
        """
        Set axis label styling options.
        :param pad: padding of the axis label
        :param size: font size of the axis label
        :param weight: font weight of the axis label
        :return:
        """
        self._update_params(
            "axis_labels",
            {
                "pad": pad,
                "size": size if size in self._font_size_options else None,
                "weight": weight if weight in self._font_weight_options else None,
            },
        )
        return self

    def set_tick_labels(
        self,
        location: str = None,
        size: str = None,
        left: bool = None,
        right: bool = None,
        bottom: bool = None,
        top: bool = None,
    ):
        """
        Set tick label styling options.
        :param location: location of the tick labels
        :param size: size of the tick label,
        :param left: whether to draw the tick labels to the left of the y-axis
        :param right: whether to draw the tick labels to the right of the y-axis
        :param bottom: whether to draw the tick labels at the bottom of the x-axis
        :param top: whether to draw the tick labels at the top of the x-axis
        :return:
        """
        self._update_params(
            "tick_labels",
            {
                "location": location if location in self._location_options else None,
                "size": size if size in self._font_size_options else None,
                "left": left,
                "right": right,
                "bottom": bottom,
                "top": top,
            },
        )
        return self

    def set_ticks(
        self,
        x_align: Optional[str] = None,
        y_align: Optional[str] = None,
        direction: Optional[str] = None,
        draw_minor: Optional[bool] = None,
        width_major: Optional[Union[float, int]] = None,
        width_minor: Optional[Union[float, int]] = None,
        size_major: Optional[Union[float, int]] = None,
        size_minor: Optional[Union[float, int]] = None,
        pad_major: Optional[Union[float, int]] = None,
        pad_minor: Optional[Union[float, int]] = None,
    ):
        """
        Set styling options for ticks.
        :param x_align:
        :param y_align:
        :param direction:
        :param draw_minor:
        :param width_major:
        :param width_minor:
        :param size_major:
        :param size_minor:
        :param pad_major:
        :param pad_minor:
        :return:
        """
        self._update_params(
            "ticks",
            {
                "x_align": x_align
                if x_align in self._horizontal_alignment_options
                else None,
                "y_align:": y_align
                if y_align in self._vertical_alignment_options
                else None,
                "direction": direction
                if direction in self._direction_options
                else None,
                "draw_minor": draw_minor,
                "width_major": width_major,
                "width_minor": width_minor,
                "size_major": size_major,
                "size_minor": size_minor,
                "pad_major": pad_major,
                "pad_minor": pad_minor,
            },
        )
        return self

    def set_lines(self, style: Optional[str] = None, width: Optional[float] = None):
        """
        Set line styling options.
        :param style: the style to draw lines with
        :param width: the width to draw lines with in pt
        :return: self
        """
        self._update_params(
            "lines",
            {
                "style": style if style in self._line_style_options else None,
                "width": width,
            },
        )
        return self

    def set_font(
        self,
        family: Optional[str] = None,
        cursive: Optional[Union[str, List[str]]] = None,
        fantasy: Optional[Union[str, List[str]]] = None,
        monospace: Optional[Union[str, List[str]]] = None,
        sans_serif: Optional[Union[str, List[str]]] = None,
        serif: Optional[Union[str, List[str]]] = None,
        size: Optional[Union[float, int]] = None,
        stretch: Optional[str] = None,
        style: Optional[str] = None,
        variant: Optional[str] = None,
        weight: Optional[Union[float, int, str]] = None,
    ):
        """
        Set font styling options.
        :param family: font family to use
        :param cursive: which font(s) to use for cursive text
        :param fantasy: which font(s) to use for fantasy text
        :param monospace: which  font(s) to use for monospace text
        :param sans_serif: which font(s) to use for sans-serif text
        :param serif: which font(s) to use for serif text
        :param size: base font size in pt that all other elements scale relative to
        :param stretch: font stretch
        :param style: font style
        :param variant: font variant
        :param weight: font weight
        :return: self
        """
        self._update_params(
            "fonts",
            {
                "family": family if family in self._font_family_options else None,
                "cursive": _wrap_list_arg(cursive),
                "fantasy": _wrap_list_arg(fantasy),
                "monospace": _wrap_list_arg(monospace),
                "sans-serif": _wrap_list_arg(sans_serif),
                "serif": _wrap_list_arg(serif),
                "size": size if (type(size) == float or type(size) == int) else None,
                "stretch": stretch if stretch in self._font_stretch_options else None,
                "style": style if style in self._font_style_options else None,
                "variant": variant if variant in self._font_variant_options else None,
                "weight": weight if weight in self._font_weight_options else None,
            },
        )
        return self

    @classmethod
    def from_file(cls, filename: str):
        with open(filename, "r") as f:
            data = json.load(f)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict):
        c = cls()
        setattr(
            c,
            "info",
            data["info"]
            if "info" in data.keys()
            else {"name": "Untitled", "description": "No description available."},
        )
        setattr(c, "params", data["params"] if "params" in data.keys() else {})
        setattr(c, "overrides", data["overrides"] if "overrides" in data.keys() else {})
        setattr(
            c, "transforms", data["transforms"] if "transforms" in data.keys() else {}
        )
        return c
