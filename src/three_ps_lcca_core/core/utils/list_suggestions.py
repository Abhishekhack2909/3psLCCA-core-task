# In core/main.py
from ..road_user_cost.carriage_width_info.carriagewayStandards import (
    CarriagewayStandards,
)
from ..road_user_cost.vehicle_operation_cost.utils import constants as v_const
from .. import standard_keys as c


def get_IRC_standard_suggestions():
    """
    Exposes Indian Road Congress (IRC) standard constraints and default values.
    Sources: IRC SP:30-2019 and IRC 106:1990.
    """

    # Manual mapping of internal keys to UI display names
    # v_const.vehicle_type_list contains[cite: 270]:
    # [c.SMALL_CARS, c.BIG_CARS, c.TWO_WHEELERS, c.BUSES, c.LCV, c.HCV, c.MCV]
    vehicle_map = [
        {"code": c.SMALL_CARS, "name": "Small Car", "fuel_type": [c.PETROL, c.DIESEL]},
        {
            "code": c.BIG_CARS,
            "name": "Big Car",
            "fuel_type": [c.PETROL, c.DIESEL],
        },
        {"code": c.TWO_WHEELERS, "name": "Two Wheeler", "fuel_type": [c.PETROL]},
        # {"code": c.BUSES, "name": "Buses", "fuel_type": [c.DIESEL]},
        {"code": c.O_BUSES, "name": "Ordinary Buses", "fuel_type": [c.DIESEL]},
        {"code": c.D_BUSES, "name": "Delux Buses", "fuel_type": [c.DIESEL]},
        {
            "code": c.LCV,
            "name": "Light Commercial Vehicle (LCV)",
            "fuel_type": [c.DIESEL],
        },
        {
            "code": c.HCV,
            "name": "Heavy Commercial Vehicle (HCV)",
            "fuel_type": [c.DIESEL],
        },
        {
            "code": c.MCV,
            "name": "Multi-Axle Commercial Vehicle (MCV)",
            "fuel_type": [c.DIESEL],
        },
    ]

    return {
        "road_geometry": {
            # Returns list of dicts with 'code', 'name', and 'width' [cite: 67, 68]
            "lane_types": CarriagewayStandards.get_suggestion(),
            "usage_note": CarriagewayStandards.NOTE,
        },
        "traffic": {
            "vehicle_options": vehicle_map,
        },
        "accident_severities": [
            {"code": c.FATAL, "name": "Fatal Accident"},
            {"code": c.MAJOR, "name": "Major Injury"},
            {"code": c.MINOR, "name": "Minor Injury"},
        ],
    }
