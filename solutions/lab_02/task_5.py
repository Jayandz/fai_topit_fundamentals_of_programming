"""Задание 5. Размеры объектов, рост списка и сравнение памяти."""
import platform
import sys
import tracemalloc


def collect_measurements():
    # Часть 1: собственные размеры шести объектов.
    sizes = [
        ['Пустой список', sys.getsizeof([])],
        ['Список 10 чисел', sys.getsizeof(list(range(10)))],
        ['Кортеж 10 чисел', sys.getsizeof(tuple(range(10)))],
        ['Строка 10 символов', sys.getsizeof('a' * 10)],
        ['Целое число 42', sys.getsizeof(42)],
        ['None', sys.getsizeof(None)],
    ]

    # Часть 2: сохраняем шаги, на которых меняется размер списка.
    numbers = []
    old_size = sys.getsizeof(numbers)
    growth = [[0, old_size]]
    for number in range(100):
        numbers.append(number)
        size = sys.getsizeof(numbers)
        if size != old_size:
            growth.append([len(numbers), size])
            old_size = size

    # Часть 3: два отдельных измерения, сначала list, затем range.
    tracemalloc.start()
    try:
        numbers = list(range(100_000))
        current, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    list_result = {'name': 'list(range(100000))', 'count': len(numbers),
                   'size': sys.getsizeof(numbers), 'current': current, 'peak': peak}
    del numbers

    tracemalloc.start()
    try:
        numbers = range(100_000)
        current, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    range_result = {'name': 'range(100000)', 'count': len(numbers),
                    'size': sys.getsizeof(numbers), 'current': current, 'peak': peak}

    if range_result['peak'] == 0:
        ratio = None
    else:
        ratio = list_result['peak'] / range_result['peak']
    return sizes, growth, [list_result, range_result], ratio


def print_report(sizes, growth, results, ratio):
    print('Среда:', platform.python_implementation(), platform.python_version())
    print('\nРазмеры объектов, байт:')
    for name, size in sizes:
        print(name, size)

    print('\nРост списка: длина и размер в байтах')
    for length, size in growth:
        print(length, size)

    for result in results:
        print('\nСценарий:', result['name'])
        print('Число элементов:', result['count'])
        print('Размер внешнего объекта, байт:', result['size'])
        print('Текущая память, КиБ:', round(result['current'] / 1024, 4))
        print('Пиковая память, КиБ:', round(result['peak'] / 1024, 4))
    if ratio is None:
        print('Отношение пиков не определено: измеренный пик range равен 0.')
    else:
        print('Отношение пиков list / range:', round(ratio, 2))
    print('КиБ = 1024 байта. Измеряются выделения после начала трассировки.')


def main():
    print('Прогноз: кортеж компактнее списка; список растёт скачками; range экономнее большого списка.')
    sizes, growth, results, ratio = collect_measurements()
    assert results[0]['count'] == 100_000
    assert results[1]['count'] == 100_000
    assert results[0]['peak'] > results[1]['peak']
    assert len(growth) < 101
    print_report(sizes, growth, results, ratio)


if __name__ == '__main__':
    main()
