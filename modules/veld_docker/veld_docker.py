from veld_core.veld_dataclasses import ExecutableVeld, ChainVeld, Veld


def build_docker_image(veld: ExecutableVeld | ChainVeld) -> ExecutableVeld | ChainVeld:
    return veld


def run_chain_veld(veld: ChainVeld):
    pass
