"""Общие измерения задания 5. Только стандартная библиотека Python."""
import platform
import sys
import tracemalloc


def measure(name, factory, count=None):
    # Объект создается после start. Размер измеряем после чтения current/peak,
    # чтобы служебный результат getsizeof не попал в пик самого сценария.
    tracemalloc.start()
    try:
        value = factory()
        current, peak = tracemalloc.get_traced_memory()
        size = sys.getsizeof(value)
        if count is None:
            count = len(value)
    finally:
        tracemalloc.stop()
    return {'name': name, 'count': count, 'size': size,
            'current': current, 'peak': peak}


def collect_measurements():
    scenarios = [
        ('Пустой список', lambda: []),
        ('Список 10 чисел', lambda: list(range(10))),
        ('Кортеж 10 чисел', lambda: tuple(range(10))),
        ('Строка 10 символов', lambda: ''.join(['a'] * 10)),
        ('Целое число', lambda: 42),
        ('None', lambda: None),
        ('list(range(100000))', lambda: list(range(100_000))),
        ('range(100000)', lambda: range(100_000)),
    ]
    measurements = []
    for name, factory in scenarios:
        count = 1 if name in ('Целое число', 'None') else None
        measurements.append(measure(name, factory, count))

    growth = []
    numbers = []
    old_size = sys.getsizeof(numbers)
    growth.append((0, old_size))
    for number in range(100):
        numbers.append(number)
        size = sys.getsizeof(numbers)
        if size != old_size:
            growth.append((len(numbers), size))
            old_size = size
    range_peak = measurements[-1]['peak']
    ratio = measurements[-2]['peak'] / range_peak if range_peak else None
    return measurements, growth, ratio


def print_report(measurements, growth, ratio):
    print('Среда:', platform.python_implementation(), platform.python_version(),
          platform.system(), platform.machine())
    print('Размеры — байты; текущая и пиковая память — КиБ (1024 байта).')
    print('Для скалярных значений число элементов условно равно 1.')
    print(f'{"Сценарий":<23} {"Число":>7} {"Размер":>8} {"Текущая":>12} {"Пиковая":>12}')
    for item in measurements:
        print(f'{item["name"]:<23} {item["count"]:>7} {item["size"]:>8} '
              f'{item["current"] / 1024:>12.4f} {item["peak"] / 1024:>12.4f}')
    print('\nРост списка (длина, размер):')
    for length, size in growth:
        print(length, size)
    if ratio is None:
        print('\nОтношение пиков list / range не определено: измеренный пик range равен 0.')
    else:
        print(f'\nОтношение пиков list / range: {ratio:.2f}')
    print('Примечание: tracemalloc учитывает выделения после start, а не всю память процесса.')
    print('Константы 42 и None уже существуют: их создание здесь не измеряется.')


def main():
    print('Прогноз: список растет скачками; list(range) требует намного больше памяти, чем range.')
    measurements, growth, ratio = collect_measurements()
    assert measurements[-2]['count'] == measurements[-1]['count'] == 100_000
    assert measurements[-2]['peak'] > measurements[-1]['peak']
    assert len(growth) < 101
    print_report(measurements, growth, ratio)


if __name__ == '__main__':
    main()
