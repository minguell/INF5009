import sys
import heapq
from collections import defaultdict
import math
import time  # Import time module for execution time measurement

class KAryHeap:
    def __init__(self, k):
        self.k = k
        self.heap = []
        self.position = {}
        self.insert_count = 0  # Counter for insert operations
        self.deletemin_count = 0  # Counter for deletemin operations
        self.decreasekey_count = 0  # Counter for decreasekey operations
    
    def push(self, key, value):
        heapq.heappush(self.heap, (value, key))
        self.position[key] = len(self.heap) - 1
        self.insert_count += 1  # Increment insert counter
    
    def pop(self):
        value, key = heapq.heappop(self.heap)
        self.position.pop(key, None)
        self.deletemin_count += 1  # Increment deletemin counter
        return key, value
    
    def decrease_key(self, key, new_value):
        for i, (val, k) in enumerate(self.heap):
            if k == key:
                self.heap[i] = (new_value, key)
                heapq.heapify(self.heap)
                self.decreasekey_count += 1  # Increment decreasekey counter
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
            return dist_u, heap  # Return the heap to access operation counts
        
        for v, weight in graph[u]:
            alt = dist_u + weight
            if alt < distances[v]:
                distances[v] = alt
                heap.push(v, alt)
                heap.decrease_key(v, alt)
    
    return "inf", heap  # Return the heap to access operation counts

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
    k = int(sys.argv[2])  # Recebe o valor de k como argumento
    
    start_time = time.time()  # Start timing
    result, heap = dijkstra(graph, source, destination, k)
    end_time = time.time()  # End timing
    
    # Print the result and performance metrics
    print(f"Result: {result}")
    print(f"Execution Time: {end_time - start_time:.6f} seconds")
    print(f"Insert Operations: {heap.insert_count}")
    print(f"DeleteMin Operations: {heap.deletemin_count}")
    print(f"DecreaseKey Operations: {heap.decreasekey_count}")