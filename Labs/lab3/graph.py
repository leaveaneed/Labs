from collections import deque

def bfs_connected(graph, start):
    """Проверяет связность графа."""
    visited = set()
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            queue.extend([neighbor for neighbor in graph[node] if neighbor not in visited])
    return len(visited) == len(graph)

def find_cycle(graph):
    """Ищет цикл в графе, возвращает цикл или None."""
    visited = set()
    parent = {}
    queue = deque([(next(iter(graph)), None)])  # (вершина, родитель)

    while queue:
        node, par = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        parent[node] = par
        for neighbor in graph[node]:
            if neighbor == par:
                continue
            if neighbor in visited:
                # Найден цикл
                cycle = []
                current = node
                while current is not None:
                    cycle.append(current)
                    current = parent[current]
                return cycle
            queue.append((neighbor, node))
    return None

def is_tree(graph):
    """Проверяет, является ли граф деревом."""
    if not bfs_connected(graph, next(iter(graph))):
        return False, "Граф несвязный"
    cycle = find_cycle(graph)
    if cycle:
        return False, f"Найден цикл: {cycle}"
    return True, "Граф является деревом"

def check_subcyclicity(graph):
    """Проверяет субцикличность графа."""
    vertices = list(graph.keys())
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            if vertices[j] not in graph[vertices[i]]:
                # Добавляем ребро
                graph[vertices[i]].append(vertices[j])
                graph[vertices[j]].append(vertices[i])

                # Проверяем наличие цикла
                cycle = find_cycle(graph)

                # Удаляем ребро
                graph[vertices[i]].remove(vertices[j])
                graph[vertices[j]].remove(vertices[i])

                # Если цикл не единственный, субцикличность нарушена
                if not cycle or len(cycle) != len(set(cycle)):
                    return False
    return True
