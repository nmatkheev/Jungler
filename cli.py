import os
import sys
import time

from clint.textui import prompt, puts, colored, validators
from parsers import parse_config
from core import Jungler
import argparse

import docker.tls as tls

# parser = argparse.ArgumentParser('backend.py')
# parser.add_argument('masterplan', type=str, help='path to masterplan.yml', metavar='-m')
# args = parser.parse_args()
#
# inputconf = args.masterplan
# masterplan = parse_config(inputconf)

def cmd_run(jungler_inst):
    """
    Start all nodes
    """
    return


def cmd_stop(jungler_inst):
    """
    Stop all nodes
    """
    return


def cmd_status(jungler_inst):
    """
    Print status info about running nodes
    """
    return


OPERATIONS = (
    ('run', cmd_run),
    ('stop', cmd_stop),
    ('status', cmd_status)
)


def setup_parser():
    parser = argparse.ArgumentParser(description='Jungler')
    parser.add_argument('masterplan', type=str, help='Masterplan.yml', metavar='-m')
    return parser

# --------------------------------- MAIN --------------------------------------
# 1 - Extract config path from command line
parser = setup_parser()
args = parser.parse_args()
configfile = args.masterplan
# 2 - Check correctness of configpath
try:
    os.stat(configfile)
except FileNotFoundError:
    puts(colored.red('Bad path to config file !!!'))
    sys.exit(1)
# 3 - Load from config entries
Config = parse_config(configfile)
app_path = Config['app_path']
data_path = Config['data_path']
docker_url = Config['docker_ip']
backends = int(Config['backends'])
test_sequence = Config['tests']
# 3.5 - Load TLS config:
CERTS = Config['tls']

tls_config = tls.TLSConfig(
    client_cert=(os.path.join(CERTS, 'cert.pem'), os.path.join(CERTS,'key.pem')),
    ca_cert=os.path.join(CERTS, 'ca.pem'),
    verify=True
)
# 4 - Create instance of Jungler class
jungler = Jungler(app_path, data_path, docker_url, backends, tls_config)

while True:
    cmd = prompt.query("What do you want?")
    if 'start' in cmd:
        jungler.start_containers_all()
        tests = Config['tests']
        for test in tests.items():
            jungler.exec_tc(test[1]['nodes'], test[1]['args'])
            time.sleep(test[1]['duration'])
    elif 'exit' in cmd:
        jungler.stop_containers_all()
        jungler.remove_containers_all()
        os.exit(0)

jungler.stop_containers_all()
jungler.remove_containers_all()