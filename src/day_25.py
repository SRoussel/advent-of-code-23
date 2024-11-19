"""Advent of code day 25 (part 2)."""

import networkx
import matplotlib

from operator import mul
from functools import reduce

def run(filename):
    """Return."""
    with open(filename) as file:
        lines = file.readlines()
    
    graph = networkx.graph.Graph()
    for line in lines:
        key, values = line.split(': ')
        values = values.strip('\n')
        values = values.split(" ")
        
        for value in values:
            graph.add_edge(key, value)

    graph.remove_edge('psj', 'fdb')
    graph.remove_edge('trh', 'ltn')
    graph.remove_edge('rmt', 'nqh')

    #networkx.draw_networkx(graph, with_labels=True)
    #matplotlib.pyplot.show()

    return reduce(mul, [len(item) for item in networkx.connected_components(graph)], 1)
