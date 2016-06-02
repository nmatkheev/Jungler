import os
import yaml


def parse_config(configfile):
    try:
        with open(configfile,'r', encoding='utf-8') as f:
            parsedict = yaml.load(f.read())
        return parsedict
    except FileNotFoundError:
        return None

