import pytest
import yaml
from sshcheckers import ssh_checkout, ssh_getout
from datetime import datetime

with open("config.yaml") as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def start_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@pytest.fixture()
def make_folders():
    return ssh_checkout(data['host'], data['user'], data['password'],f"mkdir {data['folder_tst']} {data['folder_out']} {data['folder_ext']}", "")


@pytest.fixture()
def clear_folders():
    return ssh_checkout(data['host'], data['user'], data['password'],f"rm -rf  {data['folder_tst']}/* {data['folder_out']}/* {data['folder_ext']}/*", "")


@pytest.fixture()
def make_files():
    list_files = []
    for i in range(data['count']):
        filename = f"file_{i}"
        if ssh_checkout(data['host'], data['user'], data['password'],
                f"cd {data['folder_tst']}; dd if=/dev/urandom of={filename} bs={data['bs']} count=1 iflag=fullblock",
                ""):
            list_files.append(filename)
    return list_files


@pytest.fixture()
def make_sub_folders():
    if ssh_checkout(data['host'], data['user'], data['password'],f"mkdir {data['folder_tst']}/{data['sub_folder']} ", ""):
        if ssh_checkout(data['host'], data['user'], data['password'],
                f"cd {data['folder_tst']}/{data['sub_folder']} ; dd if=/dev/urandom of=sub_file bs={data['bs']} count=1 iflag=fullblock",
                ""):
            return f"{data['sub_folder']}", "sub_file"
        else:
            return f"{data['sub_folder']}", None
    else:
        return None, None


@pytest.fixture()
def make_bad_files():
    ssh_checkout(data['host'], data['user'], data['password'],f"cd {data['folder_tst']}; 7z a {data['folder_out']}/arx2bad", "Everything is Ok")
    ssh_checkout(data['host'], data['user'], data['password'],f"truncate -s 1 {data['folder_out']}/arx2bad.7z", "")
    yield 'arx2bad.7z'
    ssh_checkout(data['host'], data['user'], data['password'],f"rm -f {data['folder_out']}/arx2bad.7z", "")


@pytest.fixture()
def save_stat():
    yield
    static_proc = ssh_getout(data['host'], data['user'], data['password'],"cat /proc/loadavg")
    stat_str = f"{datetime.now()} - количество файлов: {data['count']}, размера: {data['bs']}, статистика процессора: {static_proc}"
    ssh_getout(data['host'], data['user'], data['password'],f"echo '{stat_str}' >> {data['stat_file']}")
