from ruamel.yaml import YAML

from .shared import PROJECT_ROOT


class YAMLDoc:
    def __init__(self, filepath):
        self.filepath = filepath

    def clean(self):
        self.save(self.load())

    def load(self):
        yaml = YAML()
        yaml.default_flow_style = False
        with open(self.filepath, 'r') as yaml_handle:
            return yaml.load(yaml_handle)

    def save(self, data):
        yaml = YAML()
        yaml.indent(sequence=4, offset=2)
        yaml.default_flow_style = False
        with open(self.filepath, 'w') as yaml_handle:
            yaml.dump(data, yaml_handle)


def docs():
    data = PROJECT_ROOT / "data"

    for subdirectory in ["items", "businesses", "enclaves", "meta"]:
        path = data / subdirectory
        for item in path.glob("*.yaml"):
            yield item


if __name__ == '__main__':
    print("Loading all docs")
    for doc in docs():
        YAMLDoc(doc).clean()
