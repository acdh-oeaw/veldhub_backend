import os
from typing import Dict, List, Set, Tuple

from git import GitCommandError, Repo

from veld_core.veld_dataclasses import ChainVeld, Veld, VeldRepo
from veld_parser.veld_parser import parse_veld_yaml_content


def pull_veld_repo(repo_url) -> str:
    repo_path = None
    return repo_path


def load_veld_repos(potential_repo_path: str, veld_repo_dict: Dict = None) -> Dict[str, VeldRepo]:
    
    def build_this_veld_repo(repo) -> VeldRepo:
        
        def build_velds(commit) -> List[Veld] | None:
            
            def get_submodule_data(commit) -> List[Tuple[str, str]]:
                submodules_dict = {}
                submodules_data = []
                try:
                    submodules_refs = repo.git.show(commit.hexsha + ":./.gitmodules")
                except GitCommandError as ex:
                    pass
                else:
                    sm_path = None
                    for sm_line in submodules_refs.split("\n"):
                        path_split = sm_line.split("path = ")
                        if len(path_split) == 2:
                            sm_path = path_split[1]
                        url_split = sm_line.split("url = ")
                        if len(url_split) == 2:
                            sm_url = url_split[1]
                            submodules_dict[sm_path] = sm_url
                    commit_files = repo.git.execute(["git", "ls-tree", commit.hexsha])
                    if commit_files != "":
                        for cf in commit_files.split("\n"):
                            cf_split = cf.split("\t")
                            cf_split = cf_split[0].split(" ") + [cf_split[1]]
                            if cf_split[1] not in ["tree", "blob", "commit"]:
                                raise Exception("unhandled case")
                            elif cf_split[1] == "commit":
                                sm_url = submodules_dict.get(cf_split[3])
                                if sm_url is not None:
                                    sm_commit = cf_split[2]
                                    submodules_data.append((sm_commit, sm_url))
                return submodules_data
            
            veld_list = []
            for file_name in repo.git.show(commit.hexsha + ":./").split("\n"):
                if (
                    file_name.startswith("veld")
                ) and (
                    file_name.endswith("yaml") or file_name.endswith("yml")
                ):
                    veld = parse_veld_yaml_content(repo.git.show(commit.hexsha + ":./" + file_name))
                    if veld is not None:
                        veld.repo = veld_repo
                        veld.commit = commit.hexsha
                        veld.file_name = file_name
                        if type(veld) is ChainVeld:
                            veld.submodules_data = get_submodule_data(commit)
                        veld_list.append(veld)
            if veld_list != []:
                return veld_list
            else:
                return None

        veld_repo = VeldRepo(commits={})
        for commit in repo.iter_commits():
            veld_list = build_velds(commit)
            if veld_list is not None:
                veld_repo.commits[commit.hexsha] = veld_list
        return veld_repo
    
    if veld_repo_dict is None:
        veld_repo_dict = {}
    for dir in (
        [potential_repo_path]
        + [potential_repo_path + d for d in os.listdir(potential_repo_path)]
    ):
        try:
            repo = Repo(dir)
        except:
            print(f"not a repo: {dir}")
        else:
            veld_repo = build_this_veld_repo(repo)
            print()
    return veld_repo_dict
        
    
    
    
        
    repo = Repo(potential_repo_path)
    for commit in repo.iter_commits():
        veld_file_content = None
        submodules_dict = {}
        try:
            veld_file_name = "veld.yaml"
            veld_file_content = repo.git.show(commit.hexsha + ":./" + veld_file_name)
            veld_metadata = parse_veld_yaml_content(veld_file_content)
        except GitCommandError as ex:
            # print(ex)
            pass
        try:
            submodules_refs = repo.git.show(commit.hexsha + ":./.gitmodules")
        except GitCommandError as ex:
            # print(ex)
            pass
        else:
            sm_path = None
            sm_url = None
            for sm_line in submodules_refs.split("\n"):
                path_split = sm_line.split("path = ")
                if len(path_split) == 2:
                    sm_path = path_split[1]
                url_split = sm_line.split("url = ")
                if len(url_split) == 2:
                    sm_url = url_split[1]
                    submodules_dict[sm_path] = sm_url
        
        commit_files = repo.git.execute(["git", "ls-tree", commit.hexsha])
        if commit_files != "":
            for cf in commit_files.split("\n"):
                cf_split =  cf.split("\t")
                cf_split = cf_split[0].split(" ") + [cf_split[1]]
                if cf_split[1] not in ["tree", "blob", "commit"]:
                    raise Exception("unhandled case")
                elif cf_split[1] == "commit":
                    if submodules_dict == {}:
                        raise Exception("unhandled case")
                    sm_url = submodules_dict[cf_split[3]]
                    sm_commit = cf_split[2]
    
    return veld_repo_dict
    
    
    
    
    # repo = Repo(repo_path)
    # l = []
    # for commit in repo.iter_commits():
    #     # l.append(repo.git.show(c.hexsha + ":./README.md"))
    #     l.append(commit)
    # submodule_dir = repo.working_tree_dir + "/" + "veld_executable_ex1_fetch_json"
    # for sm in repo.submodules:
    #     print(sm.module())
    # x2 = repo.git.execute(["git", "ls-tree", "HEAD^^^^^^^^"])
    # tree = repo.tree("6636067e879e0aa52a7ac5a47450a39dbacd1bc2")
    # tree = repo.tree("29105081d7928a13c7a0e8dd6cf07eb39ed7e277")
    # # y = tree.blobs[1].data_stream.read()
    # z = list(tree.repo.submodules)
    
    
    
    # def load_current_repo(repo_path) -> VeldRepo:
    #     veld_repo = None
    #     git_repo = None
    #     for commit in git_repo:
    #         veld = parse_veld_yaml(commit)
    #     return veld_repo
    #
    # if veld_repo_dict is None:
    #     veld_repo_dict = set()
    # veld_repo = load_current_repo(repo_path)
    # veld_repo_dict.add(veld_repo)
    # for veld in veld_repo:
    #     if type(veld) is ChainVeld:
    #         veld: ChainVeld
    #         for sub_veld in veld.sub_velds:
    #             # TODO parse subrepo commit, fetch repo, parse if not yet exists in set
    #             sub_veld_repo_path = None
    #             veld_repo_dict = load_veld_repos(sub_veld_repo_path, veld_repo_dict)
    # return veld_repo_dict
