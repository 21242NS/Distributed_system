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
    escape_row = np.full(c_row.shape, n_max, dtype=np.int16)

    for iteration in range(1, n_max + 1):
        z_row[mask_row] = z_row[mask_row] ** 2 + c_row[mask_row]
        escaped = mask_row & (np.abs(z_row) > 2)
        escape_row[escaped] = iteration
        mask_row[escaped] = False

    return escape_row


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

    result = np.array(rows, dtype=np.int16)
    return result


def plot_mandelbrot(mandelbrot_set, boundaries=((-2, 2), (-2, 2))):
    (x_min, x_max), (y_min, y_max) = boundaries
    figure, axes = plt.subplots()
    image = axes.imshow(
        mandelbrot_set,
        cmap='magma',
        origin='lower',
        extent=(x_min, x_max, y_min, y_max),
        aspect='equal',
        vmin=1,
        vmax=mandelbrot_set.max(),
    )
    axes.set_xlim(x_min, x_max)
    axes.set_ylim(y_min, y_max)
    if x_min <= 0 <= x_max:
        axes.spines['left'].set_position('zero')
        axes.spines['right'].set_color('none')
        axes.yaxis.set_ticks_position('left')
    if y_min <= 0 <= y_max:
        axes.spines['bottom'].set_position('zero')
        axes.spines['top'].set_color('none')
        axes.xaxis.set_ticks_position('bottom')
    axes.set_xlabel('Re', loc='right')
    axes.set_ylabel('Im', loc='top')
    axes.set_title('Mandelbrot Set')
    figure.colorbar(image, ax=axes, label='Iterations before |z| > 2')
    figure.tight_layout()
    plt.show()
def plot_time_complete_comparaison_number_of_processes(times, n_processes_list):
    plt.plot(n_processes_list, times, marker='o')
    plt.xlabel('Number of Processes')
    plt.ylabel('Time (s)')
    plt.title('Time to Complete Mandelbrot Set Computation')
    plt.show()

def main():
    mandelbrot_set = mandelbrot(resolution=10000, n_processes=8, boundries=[(-0.9, -0.7), (0.1, 0.3)])
    plot_mandelbrot(mandelbrot_set, boundaries=[(-0.9, -0.7), (0.1, 0.3)])
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
