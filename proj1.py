#complete your tasks in this file
from dataclasses import dataclass
from typing import Any, TypeAlias

degrees:TypeAlias = float

@dataclass(frozen = True)
class GlobeRect:
    lo_lat:degrees
    hi_lat:degrees
    west_long:degrees
    east_long:degrees

@dataclass(frozen = True)
class Region:
    rect:GlobeRect
    name:str
    terrain:str

@dataclass(frozen = True)
class RegionCondition:
    region:Region
    year:int
    pop:int
    ghg_rate:float