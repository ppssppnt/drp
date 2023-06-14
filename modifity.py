import os
import sqlite3

if os.path.exists('list.sqlite'):
    os.remove('list.sqlite')
    
# Подключение к исходной базе данных
source_connection = sqlite3.connect('db.sqlite')
source_cursor = source_connection.cursor()

# Подключение к целевой базе данных
target_connection = sqlite3.connect('list.sqlite')
target_cursor = target_connection.cursor()

# Создание таблицы Drivers в целевой базе данных
target_cursor.execute('''
    CREATE TABLE IF NOT EXISTS Drivers (
        pack TEXT,
        directory TEXT,
        inf TEXT,
        ids TEXT
    )
''')

# Выборка данных из исходной таблицы
source_cursor.execute('SELECT pack, directory, inf FROM Drivers')
rows = source_cursor.fetchall()

# Вставка данных в целевую таблицу
target_cursor.executemany('INSERT INTO Drivers (pack, directory, inf) VALUES (?, ?, ?)', rows)

# Сохранение изменений в целевой базе данных
target_connection.commit()

# Закрытие соединений
source_connection.close()
target_connection.close()



# Подключение к базе данных
connection = sqlite3.connect('list.sqlite')
cursor = connection.cursor()

# Выполнение запроса для выборки данных
cursor.execute('SELECT pack, directory, inf FROM Drivers')
rows = cursor.fetchall()

# Составление пути к файлу inf
for row in rows:
    pack = row[0]
    directory = row[1]
    inf = row[2]
    inf_path = f"{pack}/{directory}/{inf}"
    print(inf_path)

# Закрытие соединения с базой данных
connection.close()

