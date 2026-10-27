"""Измерения и итоговый отчёт для задания 5."""
import platform
import sys
import tracemalloc


def measure(name):
    # Сначала включаем измерение, потом создаём нужный объект.
    tracemalloc.start()
    try:
        if name == 'Пустой список':
            value = []
        elif name == 'Список 10 чисел':
            value = list(range(10))
        elif name == 'Кортеж 10 чисел':
            value = tuple(range(10))
        elif name == 'Строка 10 символов':
            value = ''.join(['a'] * 10)
        elif name == 'Целое число':
            value = 42
        elif name == 'None':
            value = None
        elif name == 'list(range(100000))':
            value = list(range(100_000))
        elif name == 'range(100000)':
            value = range(100_000)
        else:
            raise ValueError('Неизвестный сценарий')

        current, peak = tracemalloc.get_traced_memory()
        size = sys.getsizeof(value)
        if name == 'Целое число' or name == 'None':
            count = 1  # Для одного значения условно указываем 1.
        else:
            count = len(value)
    finally:
        tracemalloc.stop()

    return {'name': name, 'count': count, 'size': size,
            'current': current, 'peak': peak}


def collect_measurements():
    names = ['Пустой список', 'Список 10 чисел', 'Кортеж 10 чисел',
             'Строка 10 символов', 'Целое число', 'None',
             'list(range(100000))', 'range(100000)']
    results = []
    for name in names:
        results.append(measure(name))

    # Запоминаем только те шаги, на которых размер списка вырос.
    numbers = []
    old_size = sys.getsizeof(numbers)
    growth = [[0, old_size]]
    for number in range(100):
        numbers.append(number)
        size = sys.getsizeof(numbers)
        if size != old_size:
            growth.append([len(numbers), size])
            old_size = size

    list_peak = results[6]['peak']
    range_peak = results[7]['peak']
    if range_peak == 0:
        ratio = None  # На ноль делить нельзя.
    else:
        ratio = list_peak / range_peak
    return results, growth, ratio


def print_report(results, growth, ratio):
    print('Среда:', platform.python_implementation(), platform.python_version())
    for result in results:
        print('\nСценарий:', result['name'])
        print('Число элементов:', result['count'])
        print('Размер внешнего объекта, байт:', result['size'])
        print('Текущая память, КиБ:', round(result['current'] / 1024, 4))
        print('Пиковая память, КиБ:', round(result['peak'] / 1024, 4))

    print('\nРост списка: длина и размер в байтах')
    for length, size in growth:
        print(length, size)
    if ratio is None:
        print('Отношение пиков не определено: измеренный пик range равен 0.')
    else:
        print('Отношение пиков list / range:', round(ratio, 2))
    print('КиБ = 1024 байта. Измеряются выделения после начала трассировки.')
    print('Нулевой результат трассировки не означает, что объект не занимает память.')


def main():
    print('Прогноз: список растёт скачками; list(range) требует больше памяти, чем range.')
    results, growth, ratio = collect_measurements()
    assert results[6]['count'] == 100_000
    assert results[7]['count'] == 100_000
    assert results[6]['peak'] > results[7]['peak']
    assert len(growth) < 101
    print_report(results, growth, ratio)


if __name__ == '__main__':
    main()
