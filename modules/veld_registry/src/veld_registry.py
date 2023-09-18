from typing import List

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
        upsert_result = db.veld.update_one(
            filter={"_id": veld_dict["_id"]},
            update={"$set": veld_dict},
            upsert=True
        )
        
    def validate(veld):
        veld_db = get_velds(_id=veld.make_db_id())
        if len(veld_db) != 1 or veld != veld_db[0]:
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
        if len(veld_repo_db) != 1 or veld_repo != veld_repo_db[0]:
            raise Exception(f"Something went wrong when persisting {veld_repo}")
        return veld_repo_db[0]
    
    persist(veld_repo)
    veld_repo = validate(veld_repo)
    return veld_repo


def get_velds(**kwargs) -> List[Veld]:
    result = list(db.veld.find(kwargs))
    veld_list = []
    for veld_dict in result:
        veld_type = veld_dict.pop("type")
        del(veld_dict["_id"])
        if veld_type == "DataVeld":
            veld_list.append(DataVeld(**veld_dict))
        elif veld_type == "ExecutableVeld":
            veld_list.append(ExecutableVeld(**veld_dict))
        elif veld_type == "ChainVeld":
            veld_list.append(ChainVeld(**veld_dict))
    return veld_list


def get_veld_repos(**kwargs) -> List[VeldRepo]:
    kwargs["_id"] = kwargs.pop("remote_url")
    result = list(
        db.veld_repo.aggregate(
            [
                {
                    "$lookup": {
                        "from": "veld",
                        "localField": "velds",
                        "foreignField": "_id",
                        "as": "velds"
                    }
                },
            ]
        )
    )
    veld_repo_list = []
    return veld_repo_list
    
    


