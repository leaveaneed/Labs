from utils import read_graph
from graph import is_tree, check_subcyclicity

def main():
    input_file = "lab3/input.txt"
    output_file = "lab3/output.txt"

    # Считываем граф
    graph = read_graph(input_file)

    # Проверяем свойства дерева
    is_tree_result, tree_message = is_tree(graph)
    subcyclicity_result = check_subcyclicity(graph)

    # Формируем вывод
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(f"Проверка свойства дерева:\n{tree_message}\n")
        if is_tree_result:
            file.write("Граф является деревом.\n")
        else:
            file.write("Граф не является деревом.\n")
        if subcyclicity_result:
            file.write("Граф древочисленный.\n")
        else:
            file.write("Граф не древочисленный.\n")

if __name__ == "__main__":
    main()
