import matplotlib.pyplot as plt
import math

def simple_plot(y_data, x_data = None, y_label = "Y", x_label = "X", title = None, filename = "plot.png"):
    if x_data == None:
        x_data = [x for x in range(len(y_data))]
    if title == None:
        title = y_label + " vs " + x_label
    assert len(x_data) == len(y_data)
    plt.figure()
    plt.plot(x_data, y_data)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.savefig(filename)