
from sshcheckers import ssh_checkout
import yaml

with open("config.yaml") as f:
    data = yaml.safe_load(f)

ssh_checkout(data['host'], data['user'], data['password'],f"mkdir {data['folder_tst']} {data['folder_out']} {data['folder_ext']}", "")