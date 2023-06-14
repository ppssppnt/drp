import subprocess
import re
import sys
import argparse

rev_enable = "YES"


def parse_hardware_string(hardware_string):
    # Определение шаблона регулярного выражения для распарсинга
    string = ""
    try:
        string += hardware_string.split("&")[0].replace("\n", "")
    except IndexError:
        string += ""
    try:
        string += "&" + hardware_string.split("&")[1].replace("\n", "")
    except IndexError:
        string += ""
    if rev_enable == "YES":
        try:
            string += "&" + hardware_string.split("&")[2].replace("\n", "")
        except IndexError:
            string += ""

    return string.replace("\n", "")


def get_hardware_info():
    # Выполнение команды "wmic" для получения списка устройств
    cmd = 'wmic path Win32_PnPEntity get PNPDeviceID'
    output = subprocess.check_output(cmd, shell=True, universal_newlines=True)

    # Обработка вывода команды
    result = ""
    for line in output.split('\n'):
        parsed_line = parse_hardware_string(line).replace("\n", "")
        if parsed_line != "":
            print(parsed_line)
            result += parsed_line + "\n"

    # Запись результатов в файл
    with open("listids.txt", "w") as file:
        file.write(result)


# Получение аргументов командной строки
args = sys.argv
# Создание парсера аргументов
parser = argparse.ArgumentParser()

# Определение аргументов
parser.add_argument("--norev", help="Отключить вывод rev id")
args = parser.parse_args()

# Использование аргументов
if args.norev is not None:
    rev_enable = "NO"

get_hardware_info()
