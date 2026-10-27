"""Задание 2. Присваивание, поверхностная и глубокая копии."""
import copy


def show(label, original, alias, shallow, deep):
    print('\n' + label)
    for name, value in [('original', original), ('alias', alias),
                        ('shallow', shallow), ('deep', deep)]:
        print(name, value)
        print('id внешнего / первой строки / первой оценки:',
              id(value), id(value[0]), id(value[0][1]))


def main():
    print('Прогноз: append увидит alias; изменение оценки увидят alias и shallow; deep сохранится.')
    original = [['Python', 5], ['Algorithms', 4]]
    alias = original
    shallow = original.copy()
    deep = copy.deepcopy(original)
    show('Исходные структуры', original, alias, shallow, deep)
    original.append(['Databases', 5])
    show('После append', original, alias, shallow, deep)
    assert len(alias) == 3 and len(shallow) == len(deep) == 2
    original[0][1] = 3
    show('После изменения оценки', original, alias, shallow, deep)
    assert alias is original and shallow is not original and deep is not original
    assert shallow[0] is original[0] and deep[0] is not original[0]
    assert shallow[0][1] == 3 and deep[0][1] == 5

    print('\nМатрицы. Прогноз: в ошибочной изменятся три строки, в правильной только первая.')
    wrong_matrix = [[0] * 3] * 3
    correct_matrix = [[0] * 3 for _ in range(3)]
    print('До:', wrong_matrix, correct_matrix)
    print('id строк ошибочной:', [id(row) for row in wrong_matrix])
    print('id строк правильной:', [id(row) for row in correct_matrix])
    wrong_matrix[0][0] = 1
    correct_matrix[0][0] = 1
    print('После:', wrong_matrix, correct_matrix)
    assert wrong_matrix == [[1, 0, 0]] * 3
    assert correct_matrix == [[1, 0, 0], [0, 0, 0], [0, 0, 0]]


if __name__ == '__main__':
    main()
