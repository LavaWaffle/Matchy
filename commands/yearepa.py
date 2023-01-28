from utils import *
from constants import *
import os
import numpy as np
import scipy as sp

NAME = "yearepa"
DESCRIPTION = "Plots the year's EPA data based on percentiles"

async def run(ctx, year: ("The year to plot", int)):
    if not os.path.exists(IMAGE_DIR):
        os.mkdir(IMAGE_DIR)
    try: data = sb.get_year(year)
    except UserWarning:
        await error(ctx, f"The EPA data for {year} does not exist.")
        return
    our_percentile = get_team_year(OUR_TEAM, year)["country_epa_percentile"] * 100
    cache.save()
    XS = np.array([0, 1, 5, 10, 25, 50, 75])
    KEYS = "epa_max epa_1p epa_5p epa_10p epa_25p epa_median epa_75p".split()
    PREFIXES = ["", "auto_", "teleop_"]
    COLORS = ["#000000", "#ff0000", "#0000ff"]
    NAMES = ["Overall", "Auto", "Teleop"]
    func = lambda x, a, b, c: a * x ** b + c
    for prefix, color, name in zip(PREFIXES, COLORS, NAMES):
        epa = np.array([data[prefix + x] for x in KEYS])
        if None in epa:
            await error(ctx, f"Could not fetch EPA data for {year}!")
            return
        popt, pcov = sp.optimize.curve_fit(func, XS, epa)
        model = lambda x: func(x, *popt)
        polyline = np.linspace(0, 100)
        plt.plot(XS, epa, "o", color=color)
        line, = plt.plot(polyline, model(polyline), color=color)
        line.set_label(name)
    plt.ylim(bottom=0)
    ylim = plt.gca().get_ylim()
    if our_percentile is not None:
        line, = plt.plot([our_percentile, our_percentile], [-1000, 10000], "--",
                         color = COLORS[0])
        line.set_label(f"Team {OUR_TEAM}'s " + NAMES[0])
    plt.xlim([0, 100])
    plt.ylim(ylim)
    plt.legend()
    plt.xlabel("Percentile")
    plt.ylabel("EPA")
    plt.title(f"Year {year}'s EPA")
    plt.grid(which = "both", axis = "both", color = "#cccccc")
    await send_plot(ctx, f"EPA data for {year}")