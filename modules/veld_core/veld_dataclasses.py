from dataclasses import asdict, dataclass, field
from typing import Dict, List, Self


# dummy class definition for VeldRepo.
# Otherwise, VeldRepo and Veld would end up in a circular dependency
class Veld:
    pass


@dataclass(kw_only=True)
class VeldRepo:
    local_path: str = None
    remote_url: str = None
    head_commit: str = None
    velds: Dict[str, List[Veld]] = None
    
    def to_dict(self):
        return asdict(self)
    
    def __iter__(self):
        for veld_list in self.velds.values():
            for veld in veld_list:
                yield veld

    def __hash__(self):
        return hash(self.remote_url)
    
    def __eq__(self, other):
        return self.to_dict() == other.to_dict()
    
    def __str__(self):
        pass
    
    def __repr__(self):
        return f"VeldRepo: {self.remote_url}"
    

@dataclass()
class Veld:
    commit: str = None
    file_name: str = None
    branch: List[str] = None
    rel_parents: List[Veld] = None
    rel_successors: List[Veld] = None
    
    def make_db_id(self):
        return self.commit + "/" + self.file_name
    
    def to_dict(self):
        return asdict(self)
    
    def __repr__(self):
        return f"Veld: {self.commit}"
    
    def __hash__(self):
        pass
    
    def __eq__(self, other):
        return self.to_dict() == other.to_dict()


@dataclass(kw_only=True)
class DataVeld(Veld):
    
    def __repr__(self):
        return f"DataVeld: {self.commit}"


@dataclass(kw_only=True)
class ExecutableVeld(Veld):
    image_digest: str = None
    
    def __repr__(self):
        return f"ExecutableVeld: {self.commit}"


@dataclass(kw_only=True)
class ChainVeld(Veld):
    image_digest: str = None
    sub_velds: List[Veld] = None
    
    def __repr__(self):
        return f"ChainVeld: {self.commit}"

