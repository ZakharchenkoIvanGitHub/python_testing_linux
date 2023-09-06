"""
Доработать функцию из предыдущего задания таким образом, чтобы у неё появился дополнительный режим
работы, в котором вывод разбивается на слова с удалением всех знаков пунктуации
(их можно взять из списка string.punctuation модуля string).
В этом режиме должно проверяться наличие слова в выводе.
"""
import re
import string
import subprocess


def test_function(command, text, full_text=True):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding="utf-8")
    if result.returncode != 0:
        return False
    if full_text:
        return text in result.stdout
    else:
        lst = result.stdout.splitlines()
        result_lst = []
        for s in lst:
            result_lst.extend([st.strip(string.punctuation) for st in re.split("=| ", s)])
        return text in result_lst


if __name__ == '__main__':
    print(test_function("cat /etc/os-release", 'Jammy', False))
    print(test_function("cat /etc/os-release", '22.04.2', False))
    print(test_function("cat /etc/os-release", '22.04.1', False))

    print(test_function("cat /etc/os-release", 'VERSION="22.04.2 LTS (Jammy Jellyfish)"'))
    print(test_function("cat /etc/os-release", 'VERSION="22.04.1 LTS (Jammy Jellyfish)"'))
