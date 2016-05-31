import yaml


def parse_config(configfile):
    with open(configfile,'r', encoding='utf-8') as f:
        parsedict = yaml.load(f.read())
    return parsedict


res = parse_config('prepare.shs')
print(res)