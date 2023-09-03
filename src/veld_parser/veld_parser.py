from veld_core.veld_dataclasses import Veld, DataVeld, ExecutableVeld, ChainVeld


def parse_veld_yaml(yaml_path) -> Veld:
    def read_schema(schema_path):
        schema = None
        return schema
    
    def parse_and_validate(yaml_path, schema) -> Veld:
        veld = None
        return veld
    
    schema = read_schema("src/veld_parser/veld_schema.txt")
    veld = parse_and_validate(yaml_path, schema)
    return veld
