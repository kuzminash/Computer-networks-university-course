
import random



count = 0

def dfs(node, been, neighbors):
    been.add(node)
    for i in range(random.randint(1, 2)):
        global count
        count += 1
        while True:
            new = f'{random.randint(0, 127)}.{random.randint(0, 127)}.{random.randint(0, 127)}.{random.randint(0, 127)}'
            if new not in been: break
        if node not in neighbors.keys(): neighbors[node] = []
        if new not in neighbors.keys(): neighbors[new] = []
        neighbors[node].append(new)
        neighbors[new].append(node)

    for child in neighbors[node]:
        if child not in been and count < 1:
            dfs(child, been, neighbors)


def generate():
    root = f'{random.randint(0, 127)}.{random.randint(0, 127)}.{random.randint(0, 127)}.{random.randint(0, 127)}'
    neighbors = {}
    been = set()
    dfs(root, been, neighbors)
    return neighbors


maxDist = 10000
def distances(neighbors):
    iteration = 0
    distance = {}
    hop_dict = {}
    for node in neighbors.keys():
        distance[node] = {}
        hop_dict[node] = {}
        for child in neighbors[node]:
            distance[node][child] = 1
            hop_dict[node][child] = child
    while True:
        iteration += 1
        has_update = False
        for source in neighbors.keys():
            for destination in neighbors.keys():
                if source == destination: continue
                for hop in neighbors[source]:
                    has_update = has_update or try_to_change(distance, hop_dict, source, destination, hop)
            print(f'{"[Source IP]":20} {"[Destination IP]":20} {"[Next Hop]":20} {"[Metric]":20}')
            for (ip, metric) in distance[source].items():
                if metric == maxDist:
                    metric = "inf"
                else:
                    metric = str(metric)

                print(f'{source:25} {ip:25} {hop_dict[source][ip]:25} {metric:25}')
        if not has_update:
            break

    print(f'RIP converged in {iteration} steps')
    for router in neighbors:
        print(f'{"[Source IP]":20} {"[Destination IP]":20} {"[Next Hop]":20} {"[Metric]":20}')
        for (ip, metric) in distance[router].items():
            if metric == maxDist:
                metric = "inf"
            else:
                metric = str(metric)

            print(f'{router:20} {ip:20} {hop_dict[router][ip]:20} {metric:20}')


def get_dist(d, f, to):
    if to in d[f]:
        return d[f][to]
    else:
        return maxDist

def try_to_change(d, h, f, to, hop):
    if get_dist(d, hop, to) + 1 < get_dist(d, f, to):
        d[f][to] = get_dist(d, hop, to) + 1
        h[f][to] = hop
        return True
    else:
        return False




a = generate()
print(a)
distances(a)


