from veld_core.veld_dataclasses import Veld, DataVeld, ExecutableVeld, ChainVeld


# TODO: make it so that the schema is only loaded once
def read_schema():
    schema_path = "src/veld_parser/veld_schema.txt"
    schema = None
    return schema


def parse_veld_yaml_content(yaml_content) -> Veld:
    schema = read_schema()
    return yaml_content
    

def parse_veld_yaml_file(yaml_path) -> Veld:
    with open(yaml_path, "r") as f:
        yaml_content = None
        veld = parse_veld_yaml_content(yaml_content)
        return veld
