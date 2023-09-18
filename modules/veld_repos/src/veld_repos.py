import os
from typing import Dict, List, Set, Tuple

from git import GitCommandError, Repo

from veld_core.veld_dataclasses import ChainVeld, Veld, VeldRepo
from veld_parser.veld_parser import parse_veld_folder


def pull_veld_repo(repo_url) -> str:
    repo_path = None
    return repo_path


# TODO: priority very low: Adapt the crawler, so that submodules must not be all pulled as well.
#  currently all submodules must be fully and recursively pulled, so that the crawler can conviently
#  crawl them. However this would lead to redundancy and higher data usage. Should data usage become
#  a problem, the crawler must be refactored.
def load_veld_repos(repos_folder: str, veld_repo_dict: Dict = None) -> Set[VeldRepo]:
    
    def build_this_veld_repo(potential_repo_path) -> VeldRepo | None:
        
        def checkout_with_submodules(repo: Repo, commit: str):
            """
            The commits need to be checked out, as well as their submodules. Simply `git show` or
            `git ls-tree` is not sufficient, because the crawler needs to go into the submodules'
            directories to fetch their remote url. Probably. Maybe there might be a more elegant
            solution?
            """
            # running verbose executes, because GitPython is buggy on occasions, and manual
            # executions seem to work more reliably.
            # Especially `repo.git.submodule('update', '--init')` causes problems
            commit_working = repo.commit().hexsha
            try:
                repo.git.execute(["git", "checkout", commit])
                repo.git.execute(["git", "submodule", "update", "--init", "--recursive"])
                repo.git.execute(["git", "clean", "-ffd"])
            except Exception as ex:
                commit_other = commit
                if commit == "main":
                    commit_other = repo.git.execute(["git", "rev-parse", commit])
                # TODO: priority very low: check if this rollback mechanism is working as intented
                #  when coping with faulty / missing commits.
                if commit_other != commit_working:
                    print(ex)
                    print("checking out previously working commit")
                    repo = checkout_with_submodules(repo, commit_working)
                else:
                    raise ex
            return repo
        
        def get_submodule_data(repo_path) -> List[Tuple[str, str]] | None:
            submodules_data = None
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
                        if submodules_data is None:
                            submodules_data = []
                        submodules_data.append((sm_commit, sm_url))
            return submodules_data
        
        veld_repo = None
        try:
            repo = Repo(potential_repo_path)
        except:
            print(f"not a repo: {potential_repo_path}")
        else:
            print(f"parsing for potential veld repo: {potential_repo_path}")
            repo = checkout_with_submodules(repo, "main")
            for commit in list(repo.iter_commits()):
                try:
                    repo = checkout_with_submodules(repo, commit.hexsha)
                except GitCommandError as ex:
                    print(ex)
                else:
                    veld_list_per_commit = parse_veld_folder(potential_repo_path)
                    if veld_list_per_commit is not None:
                        if veld_repo is None:
                            veld_repo = VeldRepo(
                                local_path=potential_repo_path,
                                remote_url=repo.remote().url,
                                velds={},
                                head_commit=commit.hexsha,
                            )
                        veld_repo.velds[commit.hexsha] = veld_list_per_commit
                        for veld in veld_list_per_commit:
                            veld.commit = commit.hexsha
                            if type(veld) is ChainVeld:
                                veld.submodules_data_tmp = get_submodule_data(potential_repo_path)
            repo = checkout_with_submodules(repo, "main")
        return veld_repo
    
    def link_sub_velds(veld_repo_dict):
        for veld_repo in veld_repo_dict.values():
            for veld in veld_repo:
                if type(veld) is ChainVeld and veld.submodules_data_tmp is not None:
                    veld: ChainVeld
                    for sm in veld.submodules_data_tmp:
                        sub_veld_repo = veld_repo_dict.get(sm[1])
                        if sub_veld_repo is None:
                            # TODO: priority medium: pull and crawl sub_veld_repo if it doesn't
                            #  exist locally yet.
                            print(f"sub_veld_repo not yet crawled: {sm[1]}")
                        else:
                            sub_veld_list = sub_veld_repo.velds[sm[0]]
                            for sub_veld in sub_veld_list:
                                if veld.sub_velds is None:
                                    veld.sub_velds = []
                                veld.sub_velds.append(sub_veld)
                    del veld.submodules_data_tmp
        return veld_repo_dict
    
    if veld_repo_dict is None:
        veld_repo_dict = {}
    if repos_folder.endswith("/"):
        repos_folder = repos_folder[:-1]
    potential_repo_list = [repos_folder + "/" + pr for pr in os.listdir(repos_folder)]
    for potential_repo_path in potential_repo_list:
        veld_repo = build_this_veld_repo(potential_repo_path)
        if veld_repo is not None:
            print(f"veld repo constructed: {potential_repo_path}")
            veld_repo_dict[veld_repo.remote_url] = veld_repo
    veld_repo_dict = link_sub_velds(veld_repo_dict)
    veld_set = set(veld_repo_dict.values())
    if len(veld_set) != len(veld_repo_dict):
        raise Exception("Somehow, redundant repos had been parsed.")
    return veld_set
    