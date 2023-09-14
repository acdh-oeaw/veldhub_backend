import os
from typing import List

from veld_core.veld_dataclasses import Veld, DataVeld, ExecutableVeld, ChainVeld
import yaml

# TODO: priority medium: Implement veld schema validator.
#  Also, make it so that the schema is only loaded once
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
    

def parse_veld_yaml_file(yaml_file_path) -> Veld | None:
    veld = None
    with open(yaml_file_path, "r") as f:
        veld = parse_veld_yaml_content(f.read())
    return veld


def parse_veld_folder(folder) -> List[Veld] | None:
    veld_list = []
    for file_name in os.listdir(folder):
        if (
            file_name.startswith("veld")
        ) and (
            file_name.endswith("yaml") or file_name.endswith("yml")
        ):
            veld = parse_veld_yaml_file(folder + "/" + file_name)
            if veld is not None:
                veld.file_name = file_name
                veld_list.append(veld)
    if veld_list != []:
        return veld_list
    else:
        return None
