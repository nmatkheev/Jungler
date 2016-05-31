import clint
from .parsers import parse_config
import docker
import argparse


parser = argparse.ArgumentParser('backend.py')
parser.add_argument('envconfpath', type=str, help='path to system.yml - description for creating environment', metavar='-s')
parser.add_argument('testplanpath', type=str, help='path to testplan.yml', metavar='-t')

args = parser.parse_args()

envconfig_raw = args.envconfpath
testplan_raw = args.testplanpath

try:
    envconf = parse_config(envconfig_raw)
    testplan = parse_config(testplan_raw)
except Exception:
    print("Bad config or test file.")
