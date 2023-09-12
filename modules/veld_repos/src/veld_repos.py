import os
from typing import Dict, List, Set, Tuple

from git import GitCommandError, Repo

from veld_core.veld_dataclasses import ChainVeld, Veld, VeldRepo
from veld_parser.veld_parser import parse_veld_yaml_content


def pull_veld_repo(repo_url) -> str:
    repo_path = None
    return repo_path


def load_veld_repos(potential_repo_path: str, veld_repo_dict: Dict = None) -> Dict[str, VeldRepo]:
    
    def build_this_veld_repo(repo, repo_path) -> VeldRepo:
        
        def checkout_with_submodules(repo, commit):
            # running verbose executes, because GitPython is buggy on occasions, and manual
            # executions seem to work more reliably.
            # Especially `repo.git.submodule('update', '--init')` causes problems
            repo.git.execute(["git", "checkout", commit])
            repo.git.execute(["git", "submodule", "update", "--init", "--recursive"])
            repo.git.execute(["git", "clean", "-ffd"])
            return repo
        
        def build_velds(repo_path) -> List[Veld] | None:
            veld_list = []
            for file_name in os.listdir(repo_path):
                if (
                    file_name.startswith("veld")
                ) and (
                    file_name.endswith("yaml") or file_name.endswith("yml")
                ):
                    with open(repo_path + "/" + file_name, "r") as f:
                        veld = parse_veld_yaml_content(f.read())
                    if veld is not None:
                        veld.file_name = file_name
                        veld_list.append(veld)
            if veld_list != []:
                return veld_list
            else:
                return None
        
        def get_submodule_data(repo_path) -> List[Tuple[str, str]]:
            submodules_data = []
            try:
                with open(repo_path + "/.gitmodules", "r") as f:
                    submodules_refs = f.read()
            except:
                pass
            else:
                for sm_line in submodules_refs.split("\n"):
                    path_split = sm_line.split("path = ")
                    if len(path_split) == 2:
                        sm_path = path_split[1]
                        subrepo = Repo(repo_path + "/" + sm_path)
                        sm_url = subrepo.remote().url
                        sm_commit = subrepo.head.commit.hexsha
                        submodules_data.append((sm_commit, sm_url))
            return submodules_data
        
        veld_repo = VeldRepo(commits={})
        repo = checkout_with_submodules(repo, "main")
        for commit in list(repo.iter_commits()):
            try:
                repo = checkout_with_submodules(repo, commit.hexsha)
            except GitCommandError as ex:
                print(ex)
            else:
                veld_list_per_commit = build_velds(repo_path)
                if veld_list_per_commit is not None:
                    veld_repo.commits[commit.hexsha] = veld_list_per_commit
                    for veld in veld_list_per_commit:
                        veld.commit = commit.hexsha
                        veld.repo = veld_repo
                        if type(veld) is ChainVeld:
                            veld.submodules_data = get_submodule_data(repo_path)
                            print(veld.submodules_data)
        repo = checkout_with_submodules(repo, "main")
        return veld_repo
    
    if veld_repo_dict is None:
        veld_repo_dict = {}
    for dir in (
        [potential_repo_path]
        + [potential_repo_path + "/" + d for d in os.listdir(potential_repo_path)]
    ):
        try:
            repo = Repo(dir)
        except:
            print(f"not a repo: {dir}")
        else:
            veld_repo = build_this_veld_repo(repo, potential_repo_path)
    return veld_repo_dict
    