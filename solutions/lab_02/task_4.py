"""Задание 4. Недостижимые циклы и ручная сборка мусора."""
import gc


def main():
    print('Автоматическая сборка включена:', gc.isenabled())
    print('Пороги:', gc.get_threshold())
    print('Статистика поколений:', gc.get_stats())
    print('\nПрогноз: после удаления внешних имен цикл останется до сборки GC.')
    gc.collect()  # Убираем мусор, накопленный до эксперимента.
    first = []
    second = []
    first.append(second)
    second.append(first)
    print('first ссылается на second:', first[0] is second)
    print('second ссылается на first:', second[0] is first)
    first_id, second_id = id(first), id(second)
    print('Запомненные id:', first_id, second_id)
    del first, second
    collected = gc.collect()
    print('Собрано после удаления имен:', collected)

    print('\nПрогноз: ручная сборка работает даже при отключенной автоматической.')
    gc.disable()
    try:
        for _ in range(5):
            cycle = []
            cycle.append(cycle)
            del cycle
        print('Автоматическая сборка включена:', gc.isenabled())
        manual = gc.collect()
        print('Собрано из пяти циклов:', manual)
        assert manual >= 5
    finally:
        gc.enable()
    print('Автоматическая сборка восстановлена:', gc.isenabled())

    print('\nГраф. Прогноз: A -> B -> C -> A недостижим; D останется доступен.')
    gc.disable()  # Не даем автоматической сборке опередить измерение.
    try:
        before = gc.collect()
        a = {'name': 'A', 'links': []}
        b = {'name': 'B', 'links': []}
        c = {'name': 'C', 'links': []}
        independent = {'name': 'D', 'links': []}
        a['links'].append(b)
        b['links'].append(c)
        c['links'].append(a)
        print('Связи:', a['name'], '->', b['name'], '->', c['name'], '->', a['name'])
        print('Независимый узел:', independent)
        del a, b, c
        after = gc.collect()
        print('Собрано до графа / после удаления графа:', before, after)
        assert after >= 6  # Три словаря и три списка связей.
        assert independent == {'name': 'D', 'links': []}
        print('После сборки узел D доступен:', independent)
    finally:
        gc.enable()
    print('Итог: GC удаляет недостижимые циклы, достижимый D сохранен.')


if __name__ == '__main__':
    main()
