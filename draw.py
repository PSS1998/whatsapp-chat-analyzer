import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
from sys import argv

def draw(file_name, divide_by_sender = False):
    times = np.load(file_name, allow_pickle=True)
    my_quarter_stats = np.zeros(24 * 4)
    if divide_by_sender:
        their_quarter_stats = np.zeros(24 * 4)

    for t in times:
        accumulated_min = t[0].hour * 60 + t[0].minute
        if divide_by_sender and not t[1]:
            their_quarter_stats[accumulated_min // 15] += 1
        else:
            my_quarter_stats[accumulated_min // 15] += 1

    x_axis = np.array(range(len(my_quarter_stats))) / 4
    figure(figsize=(18, 6), dpi=100)
    plt.xticks(np.arange(min(x_axis), max(x_axis)+2, 1))
    plt.ylabel("Number of messages")
    plt.xlabel("Time of the day (Hour)")
    plt.plot(x_axis, my_quarter_stats, label="sent")
    if divide_by_sender:
        plt.plot(x_axis, their_quarter_stats, label="received")
    plt.legend(loc="upper left")
    ylim = plt.ylim()

    for i in range(len(x_axis)):
        if i % 2 == 0:
            ymax = (my_quarter_stats[i] - ylim[0]) / (ylim[1] - ylim[0])
            if divide_by_sender:
                ymax = max(ymax, (their_quarter_stats[i] - ylim[0]) / (ylim[1] - ylim[0]))
            if i % 4 == 0:
                color = 'b'
            else:
                color = 'r'
            plt.axvline(x=x_axis[i], ymax=ymax, linewidth=0.3, c=color)

    # plt.show()
    figure_path = file_name[:-10]
    if divide_by_sender:
        figure_path += '_divided'
    plt.savefig(figure_path + '.png', bbox_inches='tight')

if __name__ == '__main__':
    file_name = input("Enter file name in which the data is saved: ")

    if len(argv) > 1:
        divide_mode = True
    else:
        divide_mode = False
    draw(file_name, divide_mode)