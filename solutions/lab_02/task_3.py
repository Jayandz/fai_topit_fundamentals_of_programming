"""Задание 3. Сильные и слабые ссылки в CPython."""
import sys
import weakref


class Record:
    pass


print('Прогноз: относительно начала счетчик изменится на +1, +2, +1, 0.')
data = [1, 2, 3]
start = sys.getrefcount(data)
print('После создания:', start)
alias = data
after_alias = sys.getrefcount(data)
print('После создания alias:', after_alias)
container = [data]
after_container = sys.getrefcount(data)
print('После помещения в контейнер:', after_container)
del alias
after_del = sys.getrefcount(data)
print('После del alias:', after_del)
container.clear()
after_clear = sys.getrefcount(data)
print('После очистки контейнера:', after_clear)
assert after_alias == start + 1
assert after_container == start + 2
assert after_del == start + 1
assert after_clear == start

print('\nПрогноз: после del record слабая ссылка вернет None.')
record = Record()
# Слабая ссылка позволяет найти объект, но не удерживает его.
weak_record = weakref.ref(record)
print('До удаления:', weak_record())
assert weak_record() is record
del record
print('После удаления:', weak_record())
assert weak_record() is None

print('\nРеестр. Прогноз: останутся first и second, затем только first.')
registry = weakref.WeakValueDictionary()
first = Record()
second = Record()
temporary = Record()
registry['first'] = first
registry['second'] = second
registry['third'] = temporary
print('Три сильные ссылки:', sorted(registry))
assert len(registry) == 3
# У третьего объекта больше не останется сильных ссылок.
del temporary
print('После удаления temporary:', sorted(registry))
assert set(registry) == {'first', 'second'}
del second
print('После удаления second:', sorted(registry))
assert set(registry) == {'first'} and registry['first'] is first
print('Итог: слабый реестр не продлевает жизнь объектов; пример применения — кеш.')

