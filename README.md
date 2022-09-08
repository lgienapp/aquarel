# Aquarel 🎨 

[![PyPi](https://img.shields.io/pypi/v/aquarel)](https://pypi.org/project/aquarel/)
[![License](https://img.shields.io/github/license/lgienapp/aquarel)]()
[![Documentation Status](https://readthedocs.org/projects/aquarel/badge/?version=latest)](https://aquarel.readthedocs.io/en/latest/?badge=latest)


Aquarel is a lightweight templating engine and wrapper around Matplotlibs' `rcparams` to make styling plots simple.
Aquarel templates can be defined programmatically and be serialized and shared in a JSON format.

Full documentation is available at [aquarel.readthedocs.io](https://aquarel.readthedocs.io/en/latest/?badge=latest).


## Installation

Install via pip:

```sh
python -m pip install aquarel
```

## Usage

###### Applying a style
Styles can be either applied globally

```python
from aquarel import load_theme

theme = load_theme("arctic_light")
theme.apply()
# ... plotting code here
theme.apply_transforms()
```
...or with a context manager:
```python
from aquarel import load_theme

with load_theme("arctic_light"):
    figure = # ... plotting code here
```

###### Transforms
Themes may specify *transforms*. Transforms are functions applied on the finished plot to achieve aesthetics that are not possibly by means of `rcparams` only.
For example, to trim the axes, one could apply the `trim` transform:
```python
from aquarel import load_theme

with load_theme("arctic_light").set_transforms(trim=True):
    figure = # ... plotting code here
    
# plt.show() or savefig() have to be called outside the context manager to have the transforms correctly applied.
figure.savefig()
```
However, there is one important thing to keep in mind: since transforms require the matplotlib figure/axes object to be present and finished, they have to be applied **after** the plotting code.
When using a theme with a context manager, this is automatically done in the `__exit__` call. If global usage is desired, `Theme.apply_transforms()` has to be called after every figure.
This also means that calls that make use of the finished figure, i.e. `plt.show` or `plt.savefig` have to commence after transform application, so **outside** the context manager.

###### Customization & Theme Creation

Besides loading a predefined theme, you can create a new theme
```python
from aquarel import Theme

theme = (
    Theme(name="demo", description="A demo theme.")
    .set_grid(draw=True, width=0.5)
    .set_font(family="monospace")
    .set_color(grid_color="blue")
)
```
...modify an existing one
```python
from aquarel import load_theme

theme = (
    load_theme("arctic_light")
    .set_grid(width=2)
)
```
...and write and load your custom styles to and from disk:
```python
from aquarel import Theme

theme = Theme.from_file("custom.json")
theme.save("custom.json")
```

If the simplified API of aquarel is not sufficient for your use-case, you can also directly modify the underlying `rcparams` with overrides:
```python
from aquarel import load_theme

theme = load_theme("arctic_light").set_overrides({
    "ytick.minor.visible": False,
    "xtick.minor.visible": True
})
```

## Themes

aquarel ships with several pre-defined themes that are designed to showcase its templating capabilities. 
Add your own with a pull request!

| Name            | Description                                                                                      | Preview                                                                              |
|:----------------|:-------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|
| `arctic_dark`   | Frosty dark theme based on the  [nord](https://github.com/arcticicestudio/nord) color scheme     | ![](https://github.com/lgienapp/aquarel/blob/main/assets/arctic_dark.png?raw=true)   |
| `arctic_light`  | Frosty dark theme based on the  [nord](https://github.com/arcticicestudio/nord) color scheme     | ![](https://github.com/lgienapp/aquarel/blob/main/assets/arctic_light.png?raw=true)  |
| `boxy_dark`     | Dark theme with enclosing box and grid                                                           | ![](https://github.com/lgienapp/aquarel/blob/main/assets/boxy_dark.png?raw=true)     |
| `boxy_light`    | Light theme with enclosing box and grid                                                          | ![](https://github.com/lgienapp/aquarel/blob/main/assets/boxy_light.png?raw=true)    |
| `minimal_dark`  | Dark theme with minimal visual elements                                                          | ![](https://github.com/lgienapp/aquarel/blob/main/assets/minimal_dark.png?raw=true)  |
| `minimal_light` | Light theme with minimal visual elements                                                         | ![](https://github.com/lgienapp/aquarel/blob/main/assets/minimal_light.png?raw=true) |
| `scientific`    | Space-efficient and color-blind friendly theme for printing on paper                             | ![](https://github.com/lgienapp/aquarel/blob/main/assets/scientific.png?raw=true)    |
| `umbra_dark`    | Balanced dark theme based on the [penumbra](https://github.com/nealmckee/penumbra) color scheme  | ![](https://github.com/lgienapp/aquarel/blob/main/assets/umbra_dark.png?raw=true)    |
| `umbra_light`   | Balanced light theme based on the [penumbra](https://github.com/nealmckee/penumbra) color scheme | ![](https://github.com/lgienapp/aquarel/blob/main/assets/umbra_light.png?raw=true)   |

## FAQ

###### How is this different from matplotlib style sheets?

`aquarel` is a wrapper around the stylesheets, so everything you can do with stylesheets can be achieved with `aquarel`. However there are some notable shortcomings of stylesheets that `aquarel` adresses:
1. **On-the-fly templating** – the stylesheets are applied once and are then used for every plot in the current plotting context (py-file, notebook, ipython session, ...). `aquarel` takes a different approach here and aims to provide per-plot styling with optional temporary changes. The style `aquarel` applies lasts throughout the context manager (`with aquarel.Theme:`), and switches back to whatever is the global default style outside of it. This allows you to do plot-level temporary changes. You have one plot in your notebook that needs no minor ticks? just `with theme.set_ticks():` for this plot only.
2. **Simplified templating**: matplotlib stylesheets have a lot of redundant keys for most applications. For example, you rarely want to have different colors for both axes; while possible with a stylefile, its cumbersome to change all the different keys to achieve a uniform look. `aquarel` simplifies this with e.x. a single `set_color(ticks="#eee")` call, which changes all related and relevant keys for ticks. Note that this simplifies the API, but does not restrict capabilities: the `set_overrides` method accepts every possible stylefile key if you want to access low-level styling.
3. **Transforms**: some style elements, like trimmed axes, are not achievable with stylesheets alone (see README for more informations). `aquarel` defines a few of these transforms (and hopefully many more in the future), and makes them persistable and shareable through aquarel themes. Instead of having to apply a seaborn despine after every plot, you can have a global style that specifies a trim, and have consistent styling throughout with minimal code repitition.
