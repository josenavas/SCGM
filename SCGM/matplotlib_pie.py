#!/usr/bin/env python

__author__ = "Joshua Shorenstein"
__copyright__ = "Copyright 2013, SCGM course project"
__credits__ = ["Joshua Shorenstein"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Joshua Shorenstein"
__email__ = "joshua.shorenstein@gmail.com"
__status__ = "Development"

import matplotlib.pyplot as plt
from os.path import splitext


def plot_pie(data, outfilepath, labels=None, plot_title=""):
    """Plots data given as a pie chart and writes it to file

    Parameters
    ----------
    data: list of floats
        Data to plot (floats between 0.0-1.0)
    outfilepath: str
        Output path and filename for chart (.png or .pdf)
    labels: list of str (optional)
        Must be in the same order as data
    plot_title: str (optional)

    Raises
    ------
    RuntimeError
        If the data and labels lists are not the same length
    ValueError
        If the output file extension is not .png or .pdf
    """
    if labels is None:
        labels = [""] * len(data)
    elif len(data) != len(labels):
        raise RuntimeError("data and labels must be same length!")

    if splitext(outfilepath).lower() not in (".png", ".pdf"):
        raise ValueError("Output must be .pdf or .png")

    #process data for graphing
    data_labels = zip(labels, data)
    data_labels.sort(reverse=True, key=lambda x: x[1])
    plot_data = [x[1]*100 for x in data_labels]
    plot_labels = [''.join([x[0], " (", '%.3e' % plot_data[pos], ")"]) for
                   pos, x in enumerate(data_labels)]

    #Create pie chart
    pie_wedges, text = plt.pie(plot_data)
    #add title, legend, and prettyness
    plt.title(plot_title)
    plt.legend(pie_wedges, plot_labels, loc="best")
    for pie_wedge in pie_wedges:
        pie_wedge.set_edgecolor('white')
    plt.axis('equal')
    plt.tight_layout()
    #save and close the current pie chart figure
    plt.savefig(outfilepath)
    plt.close()
