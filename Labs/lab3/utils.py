def read_graph(file_path):
    """Считывает граф из файла."""
    graph = {}
    with open(file_path, 'r') as file:
        for line in file:
            u, v = map(int, line.split())
            if u not in graph:
                graph[u] = []
            if v not in graph:
                graph[v] = []
            graph[u].append(v)
            graph[v].append(u)
    return graph
