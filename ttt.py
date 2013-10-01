#! /usr/bin/env python

"""
Usage:
  ttt.py <input> [-o=<output>] [-s]
  ttt.py (-h | --help)

  <input>        file with one time per line
Options:
  -h --help                 Show this screen.
  -o --output=<output>      Save the chart to this file
  -s --show                 Show the chart
"""

from docopt import docopt
import matplotlib.pyplot as plt

styles = ('r+', 'bx', '*')

def probabilites(times):
    num_times = len(times)
    y = []
    for t in times:
        y.append(float(len([v for v in times if v <= t])) / num_times)
    return y

def process_regular_file(filename):
    with open(filename, 'r') as f:
        times = f.readlines()
    times = [float(i.strip()) for i in times]
    times.sort()
    p1, = plt.plot(times, probabilites(times), 'r+')
    plt.xlabel('time (s)', fontsize=16)
    plt.ylabel('cumulative probability', fontsize=16)
    plt.legend((p1,), ('curva',),
               loc='lower right', fontsize="x-small", numpoints=1)

def process_org_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    lines = [l.strip() for l in lines if not l.startswith('|--')]  # filter frame lines
    split_lines = [l.split('|') for l in lines]
    clean_lines = [[i.strip() for i in l if i.strip()] for l in split_lines]
    columns = len(clean_lines[0])
    if not clean_lines[0][0].isdigit():
        header = clean_lines[0]
        clean_lines = clean_lines[1:]
    else:
        header = ['' for i in xrange(columns)]

    plot_lines = []
    for c in xrange(columns):
        times = [float(l[c]) for l in clean_lines]
        times.sort()
        p, = plt.plot(times, probabilites(times), styles[c])
        plot_lines.append(p)
    plt.legend(plot_lines, header,
               loc='lower right', fontsize="x-small", numpoints=1)
    plt.xlabel('time (s)', fontsize=16)
    plt.ylabel('cumulative probability', fontsize=16)


if __name__ == "__main__":
    arguments = docopt(__doc__, version='0.1')
    # print arguments
    filename = arguments['<input>']
    output = arguments['--output']
    show = arguments['--show']

    if filename.endswith('.org'):
        data = process_org_file(filename)
    else:
        data = process_regular_file(filename)

    if output:
        with open(output, 'w') as f:
            plt.savefig(f, dpi=400)
    if show:
        plt.show()
