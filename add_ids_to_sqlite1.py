import sqlite3
import py7zr
import os
import re
import chardet

# Подключение к базе данных
connection = sqlite3.connect('list.sqlite')
cursor = connection.cursor()

# Выполнение запроса для выборки данных
cursor.execute('SELECT pack, directory, inf FROM Drivers')
rows = cursor.fetchall()

# Обработка каждой строки данных
for row in rows:
    pack = row[0]
    directory = row[1]
    inf = row[2]

    archive_path = f"drivers/{pack}.7z"
    folder_path = f"{directory}/"
    file_path = f"{folder_path}{inf}"

    # Проверка существования архива
    if not os.path.exists(archive_path):
        print(f"Архив {archive_path} не существует.")
        continue

    # Открытие архива и поиск строк, содержащих "VEN_" или "DEV_"
    with py7zr.SevenZipFile(archive_path, mode='r') as archive:
        try:
            archive.extract(path='temp_folder', targets=[file_path])
            with open(f"temp_folder/{file_path}", 'rb') as file:
                # Определение кодировки файла
                raw_data = file.read()
                result = chardet.detect(raw_data)
                encoding = result['encoding']

                # Чтение файла с определенной кодировкой
                content = raw_data.decode(encoding, errors='ignore')

                # Поиск строк с использованием регулярных выражений
                matches = re.findall(r'(VEN_.+|DEV_.+)', content)
                ids = ', '.join(matches)

                # Обновление найденных строк в базе данных
                cursor.execute('UPDATE Drivers SET ids = ? WHERE (pack = ?) and (inf = ?)', (ids, pack, inf))
                connection.commit()

                print(f"Строки, содержащие 'VEN_' или 'DEV_', добавлены в БД для архива {pack}.")
        except Exception as e:
            print(f"Произошла ошибка при обработке архива {archive_path}: {str(e)}")

# Закрытие соединения с базой данных
connection.close()
