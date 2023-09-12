"""Написать функцию на Python, которой передаются в качестве параметров команда и текст.
Функция должна возвращать True, если команда успешно выполнена и текст найден в её выводе и
False в противном случае. Передаваться должна только одна строка, разбиение вывода использовать
не нужно."""

import subprocess


def test_function(command, text):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding="utf-8")
    return text in result.stdout and result.returncode == 0


if __name__ == '__main__':
    print(test_function("cat /etc/os-release", 'VERSION="22.04.2 LTS (Jammy Jellyfish)"'))
    print(test_function("cat /etc/os-release", 'VERSION="22.04.1 LTS (Jammy Jellyfish)"'))
