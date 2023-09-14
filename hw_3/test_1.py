from lib_checkout import checkout, getout
import yaml

with open("config.yaml") as f:
    data = yaml.safe_load(f)


class TestPositiv:

    def test_1(self, make_folders, clear_folders, make_files, save_stat):
        # test1 создать архив
        res1 = checkout(f"cd {data['folder_tst']}; 7z a {data['key_t']} {data['folder_out']}/{data['output_file']}",
                        "Everything is Ok")
        res2 = checkout(f"ls {data['folder_out']}; ", data['output_file'])
        assert res1 and res2, "test 1 FAIL"

    def test_2(self, clear_folders, make_files, save_stat):
        # test2 распаковать архив
        res = []
        res.append(
            checkout(f"cd {data['folder_tst']}; 7z a {data['folder_out']}/{data['output_file']}", "Everything is Ok"))
        res.append(
            checkout(f"cd {data['folder_out']}; 7z e {data['output_file']} -o{data['folder_ext']}", "Everything is Ok"))
        for file_name in make_files:
            res.append(checkout(f"ls {data['folder_ext']}; ", file_name))
        assert all(res), "test 2 FAIL"

    def test_3(self, save_stat):
        # test3 тест файла
        assert checkout(f"cd {data['folder_out']}; 7z t {data['output_file']}", "Everything is Ok"), "test 3 FAIL"

    def test_4(self, save_stat):
        # test4 обновить архив
        assert checkout(f"cd {data['folder_out']}; 7z u {data['output_file']}", "Everything is Ok"), "test 4 FAIL"

    def test_5(self):
        # test5 удаление содержимого
        assert checkout(f"cd {data['folder_out']}; 7z d {data['output_file']}", "Everything is Ok"), "test 5 FAIL"

    def test_6(self, clear_folders, make_files, save_stat):
        # test6
        res = []
        res.append(
            checkout(f"cd {data['folder_tst']}; 7z a {data['folder_out']}/{data['output_file']}", "Everything is Ok"))
        res.append(
            checkout(f"cd {data['folder_out']}; 7z e {data['output_file']} -o{data['folder_ext']}", "Everything is Ok"))
        for file_name in make_files:
            res.append(checkout(f"cd {data['folder_out']}; 7z l {data['output_file']}", file_name))
        assert all(res), "test 6 FAIL"

    def test_7(self, clear_folders, make_files, make_sub_folders, save_stat):
        # test7 распоковка с сохранением структуры
        res = []
        res.append(
            checkout(f"cd {data['folder_tst']}; 7z a {data['folder_out']}/{data['output_file']}", "Everything is Ok"))
        res.append(
            checkout(f"cd {data['folder_out']}; 7z x {data['output_file']} -o{data['folder_ext']}", "Everything is Ok"))
        for file_name in make_files:
            res.append(checkout(f"ls {data['folder_ext']}; ", file_name))

        res.append(checkout(f"ls {data['folder_ext']}; ", make_sub_folders[0]))
        res.append(checkout(f"ls {data['folder_ext']}/{make_sub_folders[0]}; ", make_sub_folders[1]))

        assert all(res), "test 7 FAIL"

    def test_8(self, clear_folders, make_files, save_stat):
        # test8 сравнение хешей
        res = []
        for file_name in make_files:
            hash_file = getout(f"cd {data['folder_tst']}; crc32 {file_name}").upper()
            res.append(checkout(f"cd {data['folder_tst']}; 7z h {file_name}", hash_file))

        assert all(res), "test 8 FAIL"
