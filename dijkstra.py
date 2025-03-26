import sys
import heapq
from collections import defaultdict
import math

class KAryHeap:
    def __init__(self, k):
        self.k = k
        self.heap = []
        self.position = {}
    
    def push(self, key, value):
        heapq.heappush(self.heap, (value, key))
        self.position[key] = len(self.heap) - 1
    
    def pop(self):
        value, key = heapq.heappop(self.heap)
        self.position.pop(key, None)
        return key, value
    
    def decrease_key(self, key, new_value):
        for i, (val, k) in enumerate(self.heap):
            if k == key:
                self.heap[i] = (new_value, key)
                heapq.heapify(self.heap)
                return
    
    def is_empty(self):
        return len(self.heap) == 0

def dijkstra(graph, source, destination, k):
    heap = KAryHeap(k)
    distances = {node: math.inf for node in graph}
    distances[source] = 0
    heap.push(source, 0)
    
    while not heap.is_empty():
        u, dist_u = heap.pop()
        
        if u == destination:
            return dist_u
        
        for v, weight in graph[u]:
            alt = dist_u + weight
            if alt < distances[v]:
                distances[v] = alt
                heap.push(v, alt)
                heap.decrease_key(v, alt)
    
    return "inf"

def parse_dimacs():
    graph = defaultdict(list)
    vertices = set()
    for line in sys.stdin:
        parts = line.split()
        if parts[0] == 'a':  # Aresta
            u, v, w = map(int, parts[1:])
            graph[u].append((v, w))
            vertices.add(u)
            vertices.add(v)
    # Ensure all vertices are in the graph, even if they have no outgoing edges
    for vertex in vertices:
        if vertex not in graph:
            graph[vertex] = []
    return graph

if __name__ == "__main__":
    graph = parse_dimacs()
    source = int(sys.argv[1])
    destination = int(sys.argv[2])
    k = int(sys.argv[3])  # Recebe o valor de k como argumento
    result = dijkstra(graph, source, destination, k)
    print(result)
