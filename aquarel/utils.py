import glob
import os
from .theme import Theme


def load_theme(theme_name: str):
    """
    Sets the chosen style and color palette globally.
    :param theme_name: name of the theme to load
    :return: the specified Theme
    :raise ValueError: if a theme is not found
    """
    themes = _get_themes()
    if theme_name in themes.keys():
        return Theme.from_file(themes[theme_name])
    else:
        raise ValueError(f"No theme named '{theme_name}' found.")


def list_themes():
    """
    Returns a list of available theme names.
    :return: a list of available theme names
    """
    return list(_get_themes().keys())


def _get_themes():
    """
    Returns available themes from the theme directory
    :return: a {name: path} dict of all available themes
    """
    loc = os.path.dirname(os.path.abspath(__file__))
    return dict(
        map(
            lambda x: (x.split("/")[-1].split(".")[0], x),
            glob.glob(f"{loc}/themes/*.json"),
        )
    )

def make_samples():
    """
    Generates sample plots for all themes to be used in documentation
    """
    import numpy as np
    import matplotlib.pyplot as plt
    for theme in list_themes():
        with load_theme(theme):
            fig, ax = plt.subplots(1, 1)
            x = np.linspace(0.0, 4.0)
            plt.plot(x, np.cos(2 * np.pi * x) * np.exp(-x))
            plt.plot(x, np.sin(2 * np.pi * x) * np.exp(-x))
            plt.plot(x, np.sin(2 * np.pi * x) * np.log(x))
            ax.set_title(theme)
            ax.set_xlabel("X-Axis")
            ax.set_ylabel("Y-Axis")
        fig.savefig(f"assets/{theme}.png", dpi=75, transparent=False, facecolor=fig.get_facecolor(),
                    bbox_inches='tight')