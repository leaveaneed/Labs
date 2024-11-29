# graph_io.py
def read_graph(filename):
    """Читает граф из файла и возвращает матрицу смежности."""
    with open(filename, 'r', encoding="utf-8") as file:
        n = int(file.readline().strip())
        graph = [[float('inf')] * n for _ in range(n)]
        
        for i in range(n):
            graph[i][i] = 0  # Кратчайший путь из вершины в саму себя

        for line in file:
            u, v, w = map(int, line.split())
            # Учитываем минимальный вес для кратных рёбер
            graph[u][v] = min(graph[u][v], w)

    return graph, n

# Функция для восстановления пути между вершинами
def reconstruct_path(i, j, next_vertex):
    """Восстанавливает путь из вершины i в вершину j."""
    if next_vertex[i][j] is None:
        return []
    path = [i]
    while i != j:
        i = next_vertex[i][j]
        path.append(i)
    return path


def write_result(filename, dist, next_vertex, n):
    """Записывает матрицу кратчайших расстояний и кратчайшие пути в файл."""
    with open(filename, 'w', encoding="utf-8") as file:
        # Записываем матрицу кратчайших расстояний
        file.write("Матрица кратчайших расстояний:\n")
        for i in range(n):
            for j in range(n):
                if dist[i][j] == float('inf'):
                    file.write("INF ")
                else:
                    file.write(f"{dist[i][j]:<5}")
            file.write("\n")

        # Записываем только существующие кратчайшие пути
        file.write("\nКратчайшие пути:\n")
        for i in range(n):
            for j in range(n):
                if i != j and dist[i][j] != float('inf'):  # Только если путь существует
                    path = reconstruct_path(i, j, next_vertex)
                    path_str = " -> ".join(map(str, path))
                    file.write(f"Путь из {i} в {j}: {path_str}\n")
