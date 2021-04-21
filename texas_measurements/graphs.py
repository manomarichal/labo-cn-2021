import matplotlib.pyplot as plt
import numpy as np

def make_bar_chart(x_axis, y_axis, title, filename):
    f = open(filename, 'w')
    f.close()
    height = y_axis
    bars = x_axis
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, height, color=(1.00,0.40,0.50, 0.8))
    plt.xticks(y_pos, [])
    plt.title(title)
    # plt.show()
    plt.savefig(filename)
