import matplotlib.pyplot as plt
import numpy as np


def rotate_ylabel(degrees: int):
    """
    Rotates the y-labels of the current plot.
    :param degrees: rotation in degrees
    """
    axes = plt.gcf().axes
    for ax_i in axes:
        ax_i.tick_params(axis='y', rotation=degrees)


def rotate_xlabel(degrees: int):
    """
    Rotates the x-labels of the current plot.
    :param degrees: rotation in degrees
    """
    axes = plt.gcf().axes
    for ax_i in axes:
        ax_i.tick_params(axis='x', rotation=degrees)


def offset(distance: int):
    """
    Offsets the plot spines.
    Code partly taken from https://github.com/mwaskom/seaborn/blob/563e96d3be1eaee8db8dfbccf7eed1f1c66dfd31/seaborn/utils.py#L292
    :param distance: offset distance int pt.
    :return:
    """
    axes = plt.gcf().axes
    for ax_i in axes:
        for side in ["top", "right", "left", "bottom"]:
            ax_i.spines[side].set_position(("outward", distance))


def trim():
    """
    Trims axes of a plot to first and last major tick.
    Code partly taken from https://github.com/mwaskom/seaborn/blob/563e96d3be1eaee8db8dfbccf7eed1f1c66dfd31/seaborn/utils.py#L292
    :return:
    """
    axes = plt.gcf().axes
    # Apply trim to all axes
    for ax_i in axes:
        # Trim x direction (bottom and top)
        xticks_major = np.asarray(ax_i.get_xticks(minor=False))
        xticks = np.asarray(ax_i.get_xticks(minor=True))
        if xticks.size:
            # Get first and last major ticks
            firsttick = np.compress(xticks_major >= min(ax_i.get_xlim()), xticks_major)[
                0
            ]
            lasttick = np.compress(xticks_major <= max(ax_i.get_xlim()), xticks_major)[
                -1
            ]
            # Trim spines to tick range
            ax_i.spines["bottom"].set_bounds(firsttick, lasttick)
            ax_i.spines["top"].set_bounds(firsttick, lasttick)
            # Update tick values for both minor and major ticks
            xticks = xticks.compress(xticks <= lasttick)
            xticks = xticks.compress(xticks >= firsttick)
            ax_i.set_xticks(xticks, minor=True)
        # Trim y direction (left and right)
        yticks_major = np.asarray(ax_i.get_yticks(minor=False))
        yticks = np.asarray(ax_i.get_yticks(minor=True))
        if yticks.size:
            # Get first and last major ticks
            firsttick = np.compress(yticks_major >= min(ax_i.get_ylim()), yticks_major)[
                0
            ]
            lasttick = np.compress(yticks_major <= max(ax_i.get_ylim()), yticks_major)[
                -1
            ]
            # Trim spines to tick range
            ax_i.spines["left"].set_bounds(firsttick, lasttick)
            ax_i.spines["right"].set_bounds(firsttick, lasttick)
            # Update tick values
            newticks = yticks.compress(yticks <= lasttick)
            newticks = newticks.compress(newticks >= firsttick)
            ax_i.set_yticks(newticks, minor=True)
