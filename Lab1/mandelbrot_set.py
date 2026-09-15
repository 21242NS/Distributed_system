import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mu
import time
import sys 
import threading as th


def _mandelbrot_row(args):
    y_value, x_values, n_max = args
    c_row = x_values + 1j * y_value
    z_row = np.zeros_like(c_row)
    mask_row = np.full(c_row.shape, True, dtype=bool)

    for _ in range(n_max):
        z_row[mask_row] = z_row[mask_row] ** 2 + c_row[mask_row]
        mask_row[np.abs(z_row) > 2] = False

    return mask_row


def mandelbrot(
    resolution,
    n_processes,
    chunk_size=8,
    boundries=[(-2, 2), (-2, 2)]
):  
    n_max = 80
    x_min, x_max = boundries[0]
    y_min, y_max = boundries[1]
    x = np.linspace(x_min, x_max, resolution)
    y = np.linspace(y_min, y_max, resolution)
    tasks = [(y_value, x, n_max) for y_value in y]
    with mu.Pool(processes=n_processes) as pool:
        rows = pool.map(_mandelbrot_row, tasks, chunksize=chunk_size)

    result = np.array(rows, dtype=bool)
    return result
def plot_mandelbrot(mandelbrot_set, boundaries=((-2, 2), (-2, 2))):
    (x_min, x_max), (y_min, y_max) = boundaries
    figure, axes = plt.subplots()
    axes.imshow(
        mandelbrot_set,
        cmap='binary',
        origin='lower',
        extent=(x_min, x_max, y_min, y_max),
        aspect='equal',
    )
    axes.set_xlim(x_min, x_max)
    axes.set_ylim(y_min, y_max)
    axes.spines['left'].set_position('zero')
    axes.spines['bottom'].set_position('zero')
    axes.spines['right'].set_color('none')
    axes.spines['top'].set_color('none')
    axes.xaxis.set_ticks_position('bottom')
    axes.yaxis.set_ticks_position('left')
    axes.set_xlabel('Re', loc='right')
    axes.set_ylabel('Im', loc='top')
    axes.set_title('Mandelbrot Set')
    figure.tight_layout()
    plt.show()
def plot_time_complete_comparaison_number_of_processes(times, n_processes_list):
    plt.plot(n_processes_list, times, marker='o')
    plt.xlabel('Number of Processes')
    plt.ylabel('Time (s)')
    plt.title('Time to Complete Mandelbrot Set Computation')
    plt.show()

def main():
    mandelbrot_set = mandelbrot(resolution=10000, n_processes=8)
    plot_mandelbrot(mandelbrot_set)
    #times = []
    #mandelbrot(resolution=10000, n_processes=n_processes)
        #time_end = time.time()
        #times.append(time_end - time_start)
    #for i in range(len(n_processes_list)):
            #print(f"Number of Processes: {n_processes_list[i]}, Time: {times[i]} seconds")
    #plot_time_complete_comparaison_number_of_processes(times, n_processes_list)
    


if __name__ == '__main__':
    mu.freeze_support()
    main()
