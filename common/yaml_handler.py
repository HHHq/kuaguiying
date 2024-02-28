import yaml

"""读取yaml配置的数据"""


def read_yaml(file):
    with open(file, encoding='utf8') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
        return data

