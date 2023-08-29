from dataclasses import dataclass


@dataclass
class Veld:
    pass


@dataclass
class DataVeld(Veld):
    pass


@dataclass
class ExecutableVeld(Veld):
    pass


@dataclass
class ChainVeld(Veld):
    pass


@dataclass
class VeldRepo:
    pass