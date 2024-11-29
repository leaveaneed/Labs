def print_matrix(matrix, n):
    """Выводит матрицу на экран в формате таблицы."""
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == float('inf'):
                print("INF", end="\t")
            else:
                print(f"{matrix[i][j]:<4}", end="\t")
        print()
