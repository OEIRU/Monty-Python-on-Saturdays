import logging
import sqlite3
import sys

test_data = [{'a': 2, 'b': 20, 'c': 'u'}, {'a': 3, 'b': 30, 'c': 'u'}, {'a': 4, 'b': 50, 'c': 'u'}]

table_name = 'test_data'

print(test_data)

r = test_data[0]

keys = list(r.keys())
print(keys)
keys = [f'{i} text' for i in keys]
print(keys)
print(','.join(keys))
sql = f"create table {table_name} ({','.join(keys)})"
print(sql)

con = sqlite3.connect('example.db')
cur = con.cursor()
try:
    cur.execute(sql)
except Exception as e:
    logging.error(f"{type(e)} {e}")
    for i in cur.execute(f'select * from {table_name}'):
        print(i)

sys.exit(0)

for r in test_data:
    columns = ",".join(list(r.keys()))
    print(columns)
    val_list = list(r.values())
    print(val_list)
    val_list = [f"'{i}'" for i in val_list]
    print(val_list)
    values = ",".join(val_list)
    print(values)
    sql = f"insert into {table_name}({columns}) values({values})"
    print(sql)
    cur.execute(sql)

con.commit()
con.close()


# create table имя_таблицы(столбец1 text, .... )
#
# insert into имя_таблицы(столбец1,....) values (значение1, значение2, .....)
#
#