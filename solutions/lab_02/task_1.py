"""Задание 1. Имена, ссылки и изменяемость."""
from copy import deepcopy


def main():
    print('A. Прогноз: сначала id равны; после a += 1 получим 11 и 10.')
    a = 10
    b = a
    print('До:', a, b, 'id:', id(a), id(b))
    a += 1
    print('После:', a, b, 'id:', id(a), id(b))
    assert a == 11 and b == 10 and a is not b

    print('\nB. Прогноз: append изменит общий список; переназначение разделит списки.')
    first = [10, 20]
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
    print('До изменения:', project, alias)
    alias['members'].append('Анна')
    alias['parameters'][0][1] = 'release'
    print('После изменения alias:', project, alias)
    assert alias is project
    independent = deepcopy(project)
    print('До изменения копии:', project, independent)
    independent['name'] = 'Второй проект'
    independent['members'].append('Иван')
    independent['parameters'][1][1] = 4
    print('После изменения копии:', project, independent)
    assert independent is not project
    assert independent['members'] is not project['members']
    assert independent['parameters'] is not project['parameters']
    assert all(x is not y for x, y in zip(project['parameters'], independent['parameters']))
    assert project['members'] == ['Лев', 'Анна']
    assert project['parameters'][1][1] == 1
    print('Итог: alias и project общие; изменяемые объекты independent независимы.')


if __name__ == '__main__':
    main()
