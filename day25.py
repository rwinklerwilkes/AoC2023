import networkx as nx
from aocd import get_data

data = get_data(day=25, year=2023)

example = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""

def parse_data(data):
    G = nx.Graph()
    for row in data.split('\n'):
        src, dest = row.split(': ')
        G.add_node(src)
        for d in dest.split(' '):
            G.add_node(d)
            G.add_edge(src, d)
    return G

def part_one(data):
    G = parse_data(data)
    edges = nx.minimum_edge_cut(G)
    G.remove_edges_from(edges)
    answer = 1
    for c in nx.connected_components(G):
        answer *= len(c)
    return answer

part_one_example_answer = part_one(example)
part_one_answer = part_one(data)