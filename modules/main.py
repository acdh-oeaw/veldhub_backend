from typing import List, Set

from veld_docker import veld_docker
from veld_core.veld_dataclasses import VeldRepo, Veld, ExecutableVeld, ChainVeld
from veld_registry.src import veld_registry
from veld_repos.src import veld_repos


def register_external_repo(repo_url) -> Set[VeldRepo]:
    repo_path = veld_repos.pull_veld_repo(repo_url)
    veld_repo_set = register_internal_repos(repo_path)
    return veld_repo_set


def register_internal_repos(repo_path) -> Set[VeldRepo]:
    veld_repo_set = veld_repos.load_veld_repos(repo_path)
    for veld_repo in veld_repo_set:
        veld_repo = veld_registry.register_veld_repo(veld_repo)
    return veld_repo_set


def build_docker_images_of_repo(veld_repo: VeldRepo) -> VeldRepo:
    for veld in veld_repo:
        if type(veld) is ExecutableVeld or type(veld) is ChainVeld:
            veld = veld_docker.build_docker_image(veld)
    return veld_repo


def run_chain_veld(veld: ChainVeld):
    veld_docker.run_chain_veld(veld)


def get_veld_repos(**kwargs) -> VeldRepo:
    return veld_registry.get_veld_repos(**kwargs)


def get_velds(**kwargs) -> Veld:
    return veld_registry.get_velds(**kwargs)
