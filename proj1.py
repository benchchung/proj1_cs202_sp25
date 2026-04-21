#complete your tasks in this file
from dataclasses import dataclass
from typing import Any, TypeAlias
import math

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
    terrain:str # "ocean" "mountains" "forest" "other"

@dataclass(frozen = True)
class RegionCondition:
    region:Region
    year:int
    pop:int
    ghg_rate:float # tons of CO₂-equivalent per year

seattle = RegionCondition((Region(GlobeRect(47.495, 47.734, -122.459, -122.224), "Seattle", "mountains")), 2026, 780000, 3500000)
tokyo = RegionCondition(Region(GlobeRect(35.528, 35.898, 139.560, 139.910), "Tokyo", "other"), 2026, 14000000, 60000000)
maldives = RegionCondition(Region(GlobeRect(-0.7, 7.1, 72.5, 74.0), "Maldives", "ocean"), 2026, 527000, 2500000)
slo = RegionCondition(Region(GlobeRect(35.05, 35.55, -120.90, -120.20), "San Luis Obispo", "mountains"), 2026, 47000, 200000)

region_conditions = [seattle, tokyo, maldives, slo]

def emissions_per_capita(rc: RegionCondition) -> float:
    if rc.pop == 0:
        return 0.0
    return rc.ghg_rate/rc.pop

def area(gr:GlobeRect):
    def deg_con(deg:float) -> float: #degree to radian helper function
        return deg * (math.pi/180)

    wrap_around_regulator = deg_con(gr.east_long) - deg_con(gr.west_long)
    if wrap_around_regulator < 0:
        wrap_around_regulator += 2 * math.pi

    a = (6378.1**2 * wrap_around_regulator * abs(math.sin(deg_con(gr.hi_lat)) - math.sin(deg_con(gr.lo_lat))))
    return a

def emissions_per_square_km(rc:RegionCondition) -> float:
    return rc.ghg_rate / area(rc.region.rect)

def densest(rc_list:list[RegionCondition]) -> str:
    if len(rc_list) == 0:
        raise IndexError("List is empty.")

    def density_checker(rc_list:list[RegionCondition]) -> RegionCondition:
        if len(rc_list) == 1:
            return rc_list[0]
        sub_max = density_checker(rc_list[1:])
        current_density = (rc_list[0].pop / area(rc_list[0].region.rect))

        if current_density > sub_max.pop/area(sub_max.region.rect):
            return rc_list[0]
        else:
            return sub_max

    return density_checker(rc_list).region.name

def project_condition(rc:RegionCondition, years:int) -> RegionCondition:
    pass