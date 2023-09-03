from typing import List, Set

from veld_core.veld_dataclasses import ChainVeld, Veld, VeldRepo
from veld_parser.veld_parser import parse_veld_yaml


def pull_veld_repo(repo_url) -> str:
    repo_path = None
    return repo_path


def load_veld_repos(repo_path, veld_repo_set=None) -> Set[VeldRepo]:
    
    def load_current_repo(repo_path) -> VeldRepo:
        veld_repo = None
        git_repo = None
        for commit in git_repo:
            veld = parse_veld_yaml(commit)
        return veld_repo
    
    if veld_repo_set is None:
        veld_repo_set = set()
    veld_repo = load_current_repo(repo_path)
    veld_repo_set.add(veld_repo)
    for veld in veld_repo:
        if type(veld) is ChainVeld:
            veld: ChainVeld
            for sub_veld in veld.sub_velds:
                # TODO parse subrepo commit, fetch repo, parse if not yet exists in set
                sub_veld_repo_path = None
                veld_repo_set = load_veld_repos(sub_veld_repo_path, veld_repo_set)
    return veld_repo_set
