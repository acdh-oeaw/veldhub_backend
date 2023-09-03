from dataclasses import dataclass, field
from typing import List, Self


# dummy class definition for VeldRepo.
# Otherwise, VeldRepo and Veld would end up in a circular dependency
class Veld:
    pass


@dataclass(kw_only=True)
class VeldRepo:
    internal_id: int
    local_path: str
    head: Veld = None

    def __iter__(self):
        pass
    
    def __next__(self):
        pass
    
    def __hash__(self):
        pass
    
    def __eq__(self, other):
        pass


@dataclass(kw_only=True)
class Veld:
    internal_id: int
    repo: VeldRepo
    commit: str
    branch: List[str]
    rel_ancestors: List[Veld] = field(default_factory=list)
    rel_successors: List[Veld] = field(default_factory=list)
    
    def __hash__(self):
        pass
    
    def __eq__(self, other):
        pass


@dataclass(kw_only=True)
class DataVeld(Veld):
    pass


@dataclass(kw_only=True)
class ExecutableVeld(Veld):
    image_digest: str


@dataclass(kw_only=True)
class ChainVeld(Veld):
    image_digest: str
    sub_velds: List[Veld]
