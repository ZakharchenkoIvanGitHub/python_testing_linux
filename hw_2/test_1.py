from lib_checkout import checkout, getout

folder_tst = "/home/ivan/tst"
folder_out = "/home/ivan/out"
folder_ext = "/home/ivan/folder1"


# cd /home/ivan/tst; 7z a ../out/arx2 test_file.txt

def test_1():
    # test1 создать архив
    res1 = checkout(f"cd {folder_tst}; 7z a ../out/arx2 test_file.txt", "Everything is Ok")
    res2 = checkout(f"ls {folder_out}; ", "arx2.7z")
    assert res1 and res2, "test 1 FAIL"


def test_2():
    # test2 распаковать архив
    res1 = checkout(f"cd {folder_out}; 7z e arx2.7z -o{folder_ext}", "Everything is Ok")
    res2 = checkout(f"ls {folder_ext}; ", "test_file.txt")
    print(res1, res2)
    assert res1 and res2, "test 2 FAIL"


def test_3():
    # test3 тест файла
    assert checkout(f"cd {folder_out}; 7z t arx2.7z", "Everything is Ok"), "test 3 FAIL"


def test_4():
    # test4 обновить архив
    assert checkout(f"cd {folder_out}; 7z u arx2.7z", "Everything is Ok"), "test 4 FAIL"


def test_5():
    # test5 удаление содержимого
    assert checkout(f"cd {folder_out}; 7z d arx2.7z", "Everything is Ok"), "test 5 FAIL"


def test_6():
    # test6 вывод списка файлов
    assert checkout(f"cd {folder_out}; 7z l arx2.7z", "test_file.txt"), "test 6 FAIL"


def test_7():
    # test7 распоковка с сохранением структуры (с путями)
    res1 = checkout(f"cd {folder_out}; 7z x arx2.7z -o{folder_ext} -y", "Everything is Ok")
    res2 = checkout(f"ls {folder_ext}; ", "test_file.txt")
    print(res1, res2)
    assert res1 and res2, "test 7 FAIL"


def test_8():
    # test8 сравнение хешей
    hash_file = getout(f"cd {folder_tst}; crc32 test_file.txt").upper()
    res1 = checkout(f"cd {folder_tst}; 7z h test_file.txt", hash_file)
    print(res1)
    assert res1, "test 8 FAIL"
