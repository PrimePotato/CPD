import yaml

with open("config.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)


def areacode_to_hood(pc):
    if pc in cfg['areacode_mapping']:
        return cfg['areacode_mapping'][pc]
    else:
        return None


def area_list():
    return cfg['areas']
