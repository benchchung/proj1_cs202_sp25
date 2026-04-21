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
#given a RegionCondition object, returns the average greenhouse gas emissions per person
#in tons of CO2 per year.

#example:
# emissions_per_capita(seattle) -> 3500000 / 780000 ~ 4.487
def emissions_per_capita(rc: RegionCondition) -> float:
    if rc.pop == 0:
        return 0.0
    return rc.ghg_rate/rc.pop

#given a GlobeRect object, this returns the surface area of the rectangular region in square kilometers

#example:
#area(GlobeRect(0, 90, 0, 90)) ~ which equates to around 1/8 of Earth's surface

def area(gr:GlobeRect) -> float:
    def deg_con(deg:float) -> float: #degree to radian helper function
        return deg * (math.pi/180)

    wrap_around_regulator = deg_con(gr.east_long) - deg_con(gr.west_long)
    if wrap_around_regulator < 0:
        wrap_around_regulator += 2 * math.pi

    a = (6378.1**2 * wrap_around_regulator * abs(math.sin(deg_con(gr.hi_lat)) - math.sin(deg_con(gr.lo_lat))))
    return a

#given a RegionCondition object, this function returns the amount of emissions per square kilometer of a region,
# in tons of CO2 per year.

#example:
# emissions_per_square_km(maldives) -> 2500000 / area(maldives.region.rect)

def emissions_per_square_km(rc:RegionCondition) -> float:
    if area(rc.region.rect) == 0:
        return 0.0
    return rc.ghg_rate / area(rc.region.rect)

#given a list of RegionCondition object, this returns the name of the region with the highest population density
# (which is population/area).

#example:
#densest([seattle, tokyo, maldives, slo]) -> "Tokyo"

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

#given a RegionCondition object, this predicts what the population and greenhouse gas emission will be in a specific
#region after x amount of years based on its terrain type, and returns a new RegionCondition object with the new values.

#example:
#project_condition(slo, 5).year -> 2031
#project_condition(slo, 5).pop  -> math.floor(47000 * (1.0005)**5)
#project_condition(slo, 5).region -> slo.region, which is unchanged.
def project_condition(rc:RegionCondition, years:int) -> RegionCondition:
    if rc.region.terrain == "ocean":
        newPopulation = math.floor(rc.pop * (1 + 0.0001)**years)
        return RegionCondition(rc.region, rc.year + years, newPopulation, newPopulation * rc.ghg_rate/rc.pop)
    elif rc.region.terrain == "mountains":
        newPopulation = math.floor(rc.pop * (1 + 0.0005) ** years)
        return RegionCondition(rc.region, rc.year + years, newPopulation, newPopulation * rc.ghg_rate / rc.pop)
    elif rc.region.terrain == "forest":
        newPopulation = math.floor(rc.pop * (1 - 0.00001) ** years)
        return RegionCondition(rc.region, rc.year + years, newPopulation, newPopulation * rc.ghg_rate / rc.pop)
    elif rc.region.terrain == "other":
        newPopulation = math.floor(rc.pop * (1 + 0.0003) ** years)
        return RegionCondition(rc.region, rc.year + years, newPopulation, newPopulation * rc.ghg_rate / rc.pop)

    newPopulation = math.floor(rc.pop * (1 + 0.0003) ** years) #this is essentially the "other" terrain growth rate but applied to non-typical terrain types
    return RegionCondition(rc.region, rc.year + years, newPopulation, newPopulation * rc.ghg_rate / rc.pop)