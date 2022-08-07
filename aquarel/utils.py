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
