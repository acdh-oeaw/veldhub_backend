from typing import Dict, List, Set

from git import GitCommandError, Repo

from veld_core.veld_dataclasses import ChainVeld, Veld, VeldRepo
from veld_parser.veld_parser import parse_veld_yaml_content


def pull_veld_repo(repo_url) -> str:
    repo_path = None
    return repo_path


def load_veld_repos(repo_path: str, veld_repo_dict: Dict = None) -> Set[VeldRepo]:
    if veld_repo_dict is None:
        veld_repo_dict = {}
        
    repo = Repo(repo_path)
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
