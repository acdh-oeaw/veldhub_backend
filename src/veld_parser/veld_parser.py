from veld_core.veld_dataclasses import Veld, DataVeld, ExecutableVeld, ChainVeld
import yaml

# TODO: make it so that the schema is only loaded once
def read_schema():
    schema_path = "src/veld_parser/veld_schema.txt"
    return None


def parse_veld_yaml_content(yaml_content) -> Veld | None:
    veld = None
    veld_yaml_dict = yaml.safe_load(yaml_content)
    if veld_yaml_dict is not None:
        veld_metadata_dict = veld_yaml_dict.get("x-veld")
        if veld_metadata_dict is not None:
            veld_type = list(veld_metadata_dict.keys())[0]
            if veld_type == "data":
                veld = DataVeld()
            elif veld_type == "executable":
                veld = ExecutableVeld()
            elif veld_type == "chain":
                veld = ChainVeld()
            else:
                print(f"Invalid VELD type: {veld_type}")
    return veld
    

def parse_veld_yaml_file(yaml_path) -> Veld:
    with open(yaml_path, "r") as f:
        yaml_content = None
        veld = parse_veld_yaml_content(yaml_content)
        return veld
