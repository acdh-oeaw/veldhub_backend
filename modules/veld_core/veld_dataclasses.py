from dataclasses import dataclass, field
from typing import Dict, List, Self


# dummy class definition for VeldRepo.
# Otherwise, VeldRepo and Veld would end up in a circular dependency
class Veld:
    pass


@dataclass(kw_only=True)
class VeldRepo:
    internal_id: int = None
    local_path: str = None
    remote_url: str = None
    head: Veld = None
    commits: Dict[str, List[Veld]] = None

    def __iter__(self):
        pass
    
    def __next__(self):
        pass
    
    def __hash__(self):
        return hash(self.remote_url)
    
    def __eq__(self, other):
        return self.remote_url == other.remote_url
    
    def __str__(self):
        pass
    
    def __repr__(self):
        return f"VeldRepo: {self.remote_url}"


@dataclass()
class Veld:
    file_name: str = None
    repo: VeldRepo = None
    commit: str = None
    branch: List[str] = None
    rel_parents: List[Veld] = None
    rel_successors: List[Veld] = None
    internal_id: int = None
    
    def __hash__(self):
        pass
    
    def __eq__(self, other):
        pass


@dataclass(kw_only=True)
class DataVeld(Veld):
    
    def __repr__(self):
        return f"DataVeld: {self.commit} at {self.repo.remote_url}"


@dataclass(kw_only=True)
class ExecutableVeld(Veld):
    image_digest: str = None
    
    def __repr__(self):
        return f"ExecutableVeld: {self.commit} at {self.repo.remote_url}"


@dataclass(kw_only=True)
class ChainVeld(Veld):
    image_digest: str = None
    sub_velds: List[Veld] = None
    
    def __repr__(self):
        return f"ChainVeld: {self.commit} at {self.repo.remote_url}"
