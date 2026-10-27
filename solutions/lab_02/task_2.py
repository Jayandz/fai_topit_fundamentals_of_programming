"""Задание 2. Копирование списков."""
import copy


def show_lists():
    # Эта функция только показывает четыре списка и их id.
    print('original:', original)
    print('alias:', alias)
    print('shallow:', shallow)
    print('deep:', deep)
    print('id внешних списков:')
    print(id(original), id(alias), id(shallow), id(deep))
    print('id первых вложенных списков:')
    print(id(original[0]), id(alias[0]), id(shallow[0]), id(deep[0]))
    print('id первых оценок:')
    print(id(original[0][1]), id(alias[0][1]), id(shallow[0][1]), id(deep[0][1]))


print('Прогноз: append увидит alias; замену оценки увидят alias и shallow; deep не изменится.')
original = [['Python', 5], ['Algorithms', 4]]
alias = original
shallow = original.copy()
deep = copy.deepcopy(original)

print('До изменений:')
show_lists()

original.append(['Databases', 5])
print('После append:')
show_lists()
assert len(alias) == 3
assert len(shallow) == 2
assert len(deep) == 2

original[0][1] = 3
print('После изменения оценки:')
show_lists()
assert alias is original
assert shallow is not original
assert shallow[0] is original[0]
assert deep[0] is not original[0]
assert shallow[0][1] == 3
assert deep[0][1] == 5

print('Прогноз: в wrong_matrix изменятся три строки, в correct_matrix только первая.')
wrong_matrix = [[0] * 3] * 3
correct_matrix = [[0] * 3 for _ in range(3)]
print('До:', wrong_matrix, correct_matrix)
print('id строк wrong_matrix:')
for row in wrong_matrix:
    print(id(row))
print('id строк correct_matrix:')
for row in correct_matrix:
    print(id(row))
wrong_matrix[0][0] = 1
correct_matrix[0][0] = 1
print('После:', wrong_matrix, correct_matrix)
assert wrong_matrix == [[1, 0, 0], [1, 0, 0], [1, 0, 0]]
assert correct_matrix == [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
