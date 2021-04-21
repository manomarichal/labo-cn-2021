import matplotlib.pyplot as plt
import numpy as np

def make_bar_chart(x_axis, y_axis, title, filename, yticks = None):
    f = open(filename, 'w')
    f.close()
    height = y_axis
    bars = x_axis
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, height, color=(1.00,0.40,0.50, 0.8))
    plt.xticks([], [])

    if yticks is None:
        yticks = [0, 5, 10, 15, 20 , 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
    plt.yticks(yticks)

    plt.title(title)
    plt.grid(b=True, axis='y', color="gray", linestyle='dashed')
    plt.savefig(filename)
    plt.show()

