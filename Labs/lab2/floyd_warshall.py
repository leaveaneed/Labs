# Алгоритм Флойда-Уоршалла с восстановлением путей
def floyd_warshall(graph, n):
    """Реализует алгоритм Флойда-Уоршалла и проверяет наличие отрицательных циклов."""
    # Инициализация матрицы расстояний и предшественников
    dist = [row[:] for row in graph]
    next_vertex = [[None if graph[i][j] == float('inf') else j for j in range(n)] for i in range(n)]

    # Основной цикл алгоритма
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] != float('inf') and dist[k][j] != float('inf'):
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_vertex[i][j] = next_vertex[i][k]

    # Проверка на наличие отрицательных циклов
    for i in range(n):
        if dist[i][i] < 0:  # Если найден отрицательный цикл
            print("Ошибка: Граф содержит отрицательный цикл.")
            return None, None  # Возвращаем None для остановки программы

    return dist, next_vertex


# Функция для восстановления пути между вершинами
def reconstruct_path(i, j, next_vertex):
    """Восстанавливает путь из вершины i в вершину j через матрицу next_vertex."""
    if next_vertex[i][j] is None:
        return []  # Нет пути

    path = [i]
    while i != j:
        i = next_vertex[i][j]
        if i is None:
            return []  # Если путь разорван, возвращаем пустой путь
        path.append(i)
    return path
