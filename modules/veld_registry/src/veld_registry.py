from typing import Dict, List

import pymongo
from bson import ObjectId
from pymongo.collection import Collection

from veld_core import settings
from veld_core.veld_dataclasses import ChainVeld, DataVeld, ExecutableVeld, Veld, VeldRepo


try:
    client = pymongo.MongoClient(
        f"mongodb://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}"
    )
    db = client[settings.db_database]
except Exception as ex:
    print(ex)
    db = None


def upsert_veld(veld: Veld) -> Veld:
    
    def persist(veld):
        veld_dict = veld.to_dict()
        veld_dict["type"] = veld.__class__.__name__
        veld_dict["_id"] = veld.make_db_id()
        if type(veld) is ChainVeld and veld.sub_velds is not None:
            veld_dict["sub_velds"] = [veld.make_db_id() for veld in veld.sub_velds]
        upsert_result = db.veld.update_one(
            filter={"_id": veld_dict["_id"]},
            update={"$set": veld_dict},
            upsert=True
        )
        
    def validate(veld):
        veld_db = get_velds(_id=veld.make_db_id())
        is_error = False
        if len(veld_db) != 1:
            is_error = True
        elif type(veld) is ChainVeld:
            veld_dict = veld.to_dict()
            veld_dict_db = veld_db[0].to_dict()
            del veld_dict["sub_velds"]
            del veld_dict_db["sub_velds"]
            if veld_dict != veld_dict_db:
                is_error = True
        elif veld != veld_db[0]:
            is_error = True
        if is_error:
            raise Exception(f"Something went wrong when persisting {veld}")
        return veld_db[0]
    
    persist(veld)
    veld = validate(veld)
    return veld


def upsert_veld_repo(veld_repo: VeldRepo) -> VeldRepo:
    
    def persist(veld_repo):
        for veld in veld_repo:
            upsert_veld(veld)
        veld_repo_dict = {
            "_id": veld_repo.remote_url,
            "local_path": veld_repo.local_path,
            "head_commit": veld_repo.head_commit,
            "velds": [veld.make_db_id() for veld in veld_repo]
        }
        upsert_result = db.veld_repo.update_one(
            filter={"_id": veld_repo.remote_url},
            update={"$set": veld_repo_dict},
            upsert=True
        )
        
    def validate(veld_repo):
        veld_repo_db = get_veld_repos(remote_url=veld_repo.remote_url)
        is_error = False
        if len(veld_repo_db) != 1:
            is_error = True
        else:
            veld_repo_dict = veld_repo.to_dict()
            veld_repo_db_dict = veld_repo_db[0].to_dict()
            for veld_list in veld_repo_dict["velds"].values():
                for veld_dict in veld_list:
                    veld_dict.pop("sub_velds", None)
            for veld_list in veld_repo_db_dict["velds"].values():
                for veld_dict in veld_list:
                    veld_dict.pop("sub_velds", None)
            if veld_repo_dict != veld_repo_db_dict:
                is_error = True
        if is_error:
            raise Exception(f"Something went wrong when persisting {veld_repo}")
        return veld_repo_db[0]
    
    persist(veld_repo)
    veld_repo = validate(veld_repo)
    return veld_repo


def build_veld_from_dict(veld_dict: Dict) -> Veld:
    veld_type = veld_dict.pop("type")
    del(veld_dict["_id"])
    if veld_type == "DataVeld":
        veld = DataVeld(**veld_dict)
    elif veld_type == "ExecutableVeld":
        veld = ExecutableVeld(**veld_dict)
    elif veld_type == "ChainVeld":
        veld = ChainVeld(**veld_dict)
    else:
        raise Exception("missing VELD type from db")
    return veld


def build_veld_repo_from_dict(veld_repo_dict: Dict) -> VeldRepo:
    veld_repo_dict["remote_url"] = veld_repo_dict.pop("_id")
    veld_dict_all = {}
    for veld_dict_single in veld_repo_dict["velds"]:
        veld = build_veld_from_dict(veld_dict_single)
        veld_list_per_commit = veld_dict_all.get(veld.commit, [])
        veld_list_per_commit.append(veld)
        veld_dict_all[veld.commit] = veld_list_per_commit
    del veld_repo_dict["velds"]
    veld_repo = VeldRepo(**veld_repo_dict)
    veld_repo.velds = veld_dict_all
    return veld_repo


def get_velds(**kwargs) -> List[Veld]:
    veld_dict_list = list(db.veld.find(kwargs))
    veld_list = []
    for veld_dict in veld_dict_list:
        veld_list.append(build_veld_from_dict(veld_dict))
    return veld_list


def get_veld_repos(**kwargs) -> List[VeldRepo]:
    kwargs["_id"] = kwargs.pop("remote_url")
    veld_repo_dict_list = list(db.veld_repo.aggregate([
        {"$match": kwargs},
        {"$lookup": {
            "from": "veld",
            "localField": "velds",
            "foreignField": "_id",
            "as": "velds"
        }}
    ]))
    veld_repo_list = []
    for veld_repo_dict in veld_repo_dict_list:
        veld_repo_list.append(build_veld_repo_from_dict(veld_repo_dict))
    return veld_repo_list
    
    


