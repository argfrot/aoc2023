from collections import Counter
from dataclasses import dataclass
from functools import reduce
from itertools import cycle
import math
import operator
import time

def get_example_input():
    with open('day_8/example.txt', 'r') as f:
        data = [parse(line) for line in f.readlines()]
    return data

def get_input():
    with open('day_8/input.txt', 'r') as f:
        data = [parse(line) for line in f.readlines()]
    return data

def parse(line):
    return line.strip()

@dataclass
class Node:
    name: str
    left: 'Node' = None
    right: 'Node' = None
    is_end: bool = False

    def __repr__(self) -> str:
        return f'{self.name} = ({self.left.name}, {self.right.name})'

def get_node(node_name, nodes):
    if node_name not in nodes:
           nodes[node_name] = Node(node_name)
    return nodes[node_name]

def clean_name(name):
    return name.replace('(', '').replace(')', '').replace(',', '')

def build_graph(data):
    nodes = {}

    for line in data:
        l = line.split()

        node = get_node(l[0], nodes)
        left_node = get_node(clean_name(l[2]), nodes)
        right_node = get_node(clean_name(l[3]), nodes)

        node.left = left_node
        node.right = right_node

    return nodes

def search(start, end, graph, path):
    node = graph[start]
    path = cycle(path)
    steps = 0
    while node.name != end:
        step = next(path)
        node = node.left if step == 'L' else node.right
        steps += 1
    return steps

def reached_end(current_nodes, end_nodes):
    return all(n.is_end for n in current_nodes)

# naive, too slow
def search_all(start_char, end_char, graph, path):
    start_nodes = [graph[n] for n in graph if n.endswith(start_char)]
    end_nodes = [graph[n] for n in graph if n.endswith(end_char)]

    for node in end_nodes:
        node.is_end = True

    path = cycle(path)
    steps = 0
    t = time.time()

    current_nodes = start_nodes

    while not (reached_end(current_nodes, end_nodes)):
        step = next(path)
        next_nodes = []
        for node in current_nodes:
            next_node = node.left if step == 'L' else node.right
            next_nodes.append(next_node)
        current_nodes = next_nodes
        steps += 1
        if steps % 100000 == 0:
            t_now = time.time()
            print(f'{steps=} {len(current_nodes)=} {(t_now - t)}s')
            t = t_now

    return steps


def find_period(start, graph, path):
    node = graph[start]
    path = cycle(path)
    return_steps = []

    end_nodes_on_path = []
    steps = 0

    # take the first step away from start
    step = next(path)
    node = node.left if step == 'L' else node.right
    steps += 1
    if node.name.endswith('Z'):
        end_nodes_on_path.append(node.name)

    while node.name != start:
        step = next(path)
        node = node.left if step == 'L' else node.right
        steps += 1
        if node.name.endswith('Z'):
            end_nodes_on_path.append(node.name)

    return_steps.append(steps)

    steps = 0

    # make sure it stays the same
    # take the first step away from start
    step = next(path)
    node = node.left if step == 'L' else node.right
    steps += 1
    if node.name.endswith('Z'):
        end_nodes_on_path.append(node.name)

    while node.name != start:
        step = next(path)
        node = node.left if step == 'L' else node.right
        steps += 1
        if node.name.endswith('Z'):
            end_nodes_on_path.append(node.name)

    return_steps.append(steps)

    return return_steps, end_nodes_on_path


def find_first_end_node(start, graph, path):
    node = graph[start]
    path = cycle(path)
    steps = 0

    while not node.name.endswith('Z'):
        step = next(path)
        node = node.left if step == 'L' else node.right
        steps += 1

    return steps, node.name

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

def lcm_list(l):
    return reduce(lcm, l, 1)

if __name__ == '__main__':
    data = get_input()

    path = data[0].strip()
    graph = build_graph(data[2:])

    # part 1 - 21251
    #print(search('AAA', 'ZZZ', graph, path))

    # part 2 - ???? - naive, too slow
    #print(search_all('A', 'Z', graph, path))

    # part 2 - 11678319315857
    # explore the period it takes to return to the end_node
    start_nodes = [graph[n] for n in graph if n.endswith('A')]
    end_nodes = [graph[n] for n in graph if n.endswith('Z')]

    # print(start_nodes)
    # print(end_nodes)

    steps_to_return = []
    for end_node in end_nodes:
        period, end_nodes_on_path = find_period(end_node.name, graph, path)
        print(f'{end_node=} {period} {len(path)} {list([p/len(path) for p in period])} {end_nodes_on_path}')
        steps_to_return.append(period[0])

    for start_node in start_nodes:
        steps, end_node = find_first_end_node(start_node.name, graph, path)
        print(f'{start_node=} {steps} {steps/len(path)} {end_node}')

    # l_pathiters = lcm_list([59, 79, 61, 43, 67, 53])
    # l_steps = lcm_list([15871, 21251, 16409, 11567, 18023, 14257])
    # print(l_pathiters)
    # print(l_steps)
    # print(l_pathiters*len(path))

    print(lcm_list(steps_to_return))
