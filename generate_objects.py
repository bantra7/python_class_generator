import argparse
import yaml
import os


def get_objects_config(filename="objects.yaml"):
    """
    Setup configuration
    Returns config from a file.yaml
    :return: configuration
    :rtype: dict
    """
    config = {}
    if os.path.exists(filename):
        with open(filename, 'rt') as f:
            config.update(yaml.safe_load(f.read()))
    return config


def write_with_tabs(file, line, number_tab):
    new_line = '{}{}'.format('    '*number_tab, line)
    # new_line = '{}{}'.format(''.join(['\t'] * number_tab), line)
    file.write(new_line)


def main():
    parser = argparse.ArgumentParser(description='Generate Python objects from yaml')
    parser.add_argument('--inputfile', type=str, default='objects.yaml',
                        help='input file in yaml')

    args = parser.parse_args()
    objects_config = get_objects_config(args.inputfile)
    for model_name, model in objects_config['models'].items():
        model_filename = '{}.py'.format(model_name.lower())
        model_attributes = model.get('attributes', [])
        model_methods = model.get('methods', [])
        tab = 0
        with open(model_filename, 'w') as f:
            line = 'class {}(object):\n'.format(model_name)
            write_with_tabs(f, line, tab)
            write_with_tabs(f, '\n', tab)
            tab += 1
            line = 'def __init__(self,{}):\n'.format(', '.join(model_attributes))
            write_with_tabs(f, line, tab)
            tab += 1
            for attribute in model_attributes:
                line = 'self.{} = {}\n'.format(attribute, attribute)
                write_with_tabs(f, line, tab)
            tab -= 1
            write_with_tabs(f, '\n', tab)
            for method in model_methods:
                line = 'def {}(self):\n'.format(method)
                write_with_tabs(f, line, tab)
                tab += 1
                line = 'return \'\'\n'
                write_with_tabs(f, line, tab)
                tab -= 1
                write_with_tabs(f, '\n', tab)




if __name__ == '__main__':
    main()
