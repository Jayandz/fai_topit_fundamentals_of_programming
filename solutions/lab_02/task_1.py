"""Задание 1. Имена, ссылки и изменяемость."""
from copy import deepcopy


print('A. Прогноз: сначала id равны; после a += 1 получим 11 и 10.')
# Число нельзя изменить на месте.
a = 10
b = a
print('До:', a, b, 'id:', id(a), id(b))
a += 1
print('После:', a, b, 'id:', id(a), id(b))
assert a == 11 and b == 10 and a is not b

print('\nB. Прогноз: append изменит общий список; переназначение разделит списки.')
first = [10, 20]
# Здесь оба имени указывают на один список.
second = first
print('До append:', first, second, 'id:', id(first), id(second))
second.append(30)
print('После append:', first, second, 'id:', id(first), id(second))
assert first is second and first == [10, 20, 30]
second = [10, 20, 30]
print('После переназначения:', first, second, 'id:', id(first), id(second))
print('==:', first == second, 'is:', first is second)
assert first == second and first is not second
second.append(40)
print('После изменения нового списка:', first, second)
assert first == [10, 20, 30] and second == [10, 20, 30, 40]

print('\nКонфигурации. Прогноз: присваивание оставляет объекты общими, deepcopy изолирует изменения.')
project = {'name': 'Учебный проект', 'members': ['Лев'],
           'parameters': [['mode', 'debug'], ['workers', 1]]}
alias = project
print('project до:', project)
print('alias до:', alias)
alias['members'].append('Анна')
alias['parameters'][0][1] = 'release'
print('project после:', project)
print('alias после:', alias)
assert alias is project
# Копируем и словарь, и вложенные списки.
independent = deepcopy(project)
print('project до:', project)
print('independent до:', independent)
independent['name'] = 'Второй проект'
independent['members'].append('Иван')
independent['parameters'][1][1] = 4
print('project после:', project)
print('independent после:', independent)
assert independent is not project
assert independent['members'] is not project['members']
assert independent['parameters'] is not project['parameters']
assert independent['parameters'][0] is not project['parameters'][0]
assert independent['parameters'][1] is not project['parameters'][1]
assert project['members'] == ['Лев', 'Анна']
assert project['parameters'][1][1] == 1
print('Итог: alias и project общие; изменяемые объекты independent независимы.')

