import yaml
from sshcheckers import ssh_checkout, upload_files, ssh_getout

with open("config.yaml") as f:
    data = yaml.safe_load(f)


class TestPositiv:

    def save_log(self, start_time, name):
        with open(name, "w") as f:
            f.write(ssh_getout(data['host'], data['user'], data['password'], f"journalctl --since '{start_time}'"))

    def test_0(self, start_time):
        res = []
        upload_files(data['host'], data['user'], data['password'], data['local_path'], data['remote_path'])
        res.append(ssh_checkout(data['host'], data['user'], data['password'], "echo '123' | sudo -S dpkg -i p7zip.deb",
                                "Настраивается пакет"))
        res.append(ssh_checkout(data['host'], data['user'], data['password'], "echo '123' | sudo -S dpkg -s p7zip-full",
                                "Status: install ok installed"))
        self.save_log(start_time, 'test_log.txt')

        assert all(res), "test 0 FAIL"

    def test_1(self, make_folders, clear_folders, make_files, save_stat, start_time):
        # test1 создать архив
        res = []
        res.append(ssh_checkout(data['host'], data['user'], data['password'],
                                f"cd {data['folder_tst']}; 7z a {data['key_t']} {data['folder_out']}/{data['output_file']}",
                                "Everything is Ok"))
        res.append(ssh_checkout(data['host'], data['user'], data['password'], f"ls {data['folder_out']}; ",
                                data['output_file']))
        self.save_log(start_time, 'test_log.txt')

        assert all(res), "test 1 FAIL"

    def test_2(self, clear_folders, make_files, save_stat):
        # test2 распаковать архив
        res = []
        res.append(
            ssh_checkout(data['host'], data['user'], data['password'],
                         f"cd {data['folder_tst']}; 7z a {data['folder_out']}/{data['output_file']}",
                         "Everything is Ok"))
        res.append(
            ssh_checkout(data['host'], data['user'], data['password'],
                         f"cd {data['folder_out']}; 7z e {data['output_file']} -o{data['folder_ext']}",
                         "Everything is Ok"))
        for file_name in make_files:
            res.append(
                ssh_checkout(data['host'], data['user'], data['password'], f"ls {data['folder_ext']}; ", file_name))
        assert all(res), "test 2 FAIL"

    def test_3(self, save_stat):
        # test3 тест файла
        assert ssh_checkout(data['host'], data['user'], data['password'],
                            f"cd {data['folder_out']}; 7z t {data['output_file']}", "Everything is Ok"), "test 3 FAIL"

    def test_4(self, save_stat):
        # test4 обновить архив
        assert ssh_checkout(data['host'], data['user'], data['password'],
                            f"cd {data['folder_out']}; 7z u {data['output_file']}", "Everything is Ok"), "test 4 FAIL"

    def test_5(self):
        # test5 удаление содержимого
        assert ssh_checkout(data['host'], data['user'], data['password'],
                            f"cd {data['folder_out']}; 7z d {data['output_file']}", "Everything is Ok"), "test 5 FAIL"

    def test_6(self, clear_folders, make_files, save_stat):
        # test6
        res = []
        res.append(
            ssh_checkout(data['host'], data['user'], data['password'],
                         f"cd {data['folder_tst']}; 7z a {data['folder_out']}/{data['output_file']}",
                         "Everything is Ok"))
        res.append(
            ssh_checkout(data['host'], data['user'], data['password'],
                         f"cd {data['folder_out']}; 7z e {data['output_file']} -o{data['folder_ext']}",
                         "Everything is Ok"))
        for file_name in make_files:
            res.append(ssh_checkout(data['host'], data['user'], data['password'],
                                    f"cd {data['folder_out']}; 7z l {data['output_file']}", file_name))
        assert all(res), "test 6 FAIL"

    def test_7(self, clear_folders, make_files, make_sub_folders, save_stat):
        # test7 распоковка с сохранением структуры
        res = []
        res.append(
            ssh_checkout(data['host'], data['user'], data['password'],
                         f"cd {data['folder_tst']}; 7z a {data['folder_out']}/{data['output_file']}",
                         "Everything is Ok"))
        res.append(
            ssh_checkout(data['host'], data['user'], data['password'],
                         f"cd {data['folder_out']}; 7z x {data['output_file']} -o{data['folder_ext']}",
                         "Everything is Ok"))
        for file_name in make_files:
            res.append(
                ssh_checkout(data['host'], data['user'], data['password'], f"ls {data['folder_ext']}; ", file_name))

        res.append(ssh_checkout(data['host'], data['user'], data['password'], f"ls {data['folder_ext']}; ",
                                make_sub_folders[0]))
        res.append(ssh_checkout(data['host'], data['user'], data['password'],
                                f"ls {data['folder_ext']}/{make_sub_folders[0]}; ", make_sub_folders[1]))

        assert all(res), "test 7 FAIL"

    def test_8(self, clear_folders, make_files, save_stat):
        # test8 сравнение хешей
        res = []
        for file_name in make_files:
            hash_file = ssh_getout(data['host'], data['user'], data['password'],
                                   f"cd {data['folder_tst']}; crc32 {file_name}").upper()
            res.append(
                ssh_checkout(data['host'], data['user'], data['password'], f"cd {data['folder_tst']}; 7z h {file_name}",
                             hash_file))

        assert all(res), "test 8 FAIL"

    def test_9(self, start_time):
        res = []
        res.append(ssh_checkout(data['host'], data['user'], data['password'], "echo '123' | sudo -S dpkg -r p7zip-full",
                                "Удаляется p7zip-full"))
        res.append(ssh_checkout(data['host'], data['user'], data['password'], "echo '123' | sudo -S dpkg -s p7zip-full",
                                "Status: deinstall ok"))
        self.save_log(start_time, 'test_log.txt')
        assert all(res), "test 9 FAIL"
