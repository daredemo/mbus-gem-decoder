"""Type constants for MBUS-GEM data conversion
"""

__version__ = "0.1.0"
__author__ = "René"

from enum import Enum


class RegisterType(Enum):
    """
    Enumerator for register types.

    |   KEY       |VALUE|
    |:------------|----:|
    | METER_ENTRY | 0   |
    | MBUS_GEM    | 1   |
    | METER       | 2   |
    """

    METER_ENTRY = 0
    MBUS_GEM = 1
    METER = 2


class MeterFlag(Enum):
    """
    Enumerator for meter status messages.

    |   KEY                 |VALUE|
    |:----------------------|----:|
    |READ_SUCCESS           | 0   |
    |READ_FAILURE           | 1   |
    |VALUES_UPDATED_SUCCESS | 2   |
    |VALUES_UPDATE_FAILURE  | 3   |
    """

    READ_SUCCESS = 0
    READ_FAILURE = 1
    VALUES_UPDATED_SUCCESS = 2
    VALUES_UPDATE_FAILURE = 3


class ReadabilityTypes(Enum):
    """
    | KEY          |VALUE|
    |:-------------|----:|
    |SHORT         | 0   |
    |HUMAN_READABLE| 1   |
    |BOTH          | 2   |
    """

    SHORT = 0
    HUMAN_READABLE = 1
    BOTH = 2


MEDIUM_TYPES = [
    {"num": 0, "name": "Other"},
    {"num": 1, "name": "Oil"},
    {"num": 2, "name": "Electricity"},
    {"num": 3, "name": "Gas"},
    {"num": 4, "name": "Heat (outlet)"},
    {"num": 5, "name": "Steam"},
    {"num": 6, "name": "Warm water"},
    {"num": 7, "name": "Water"},
    {"num": 8, "name": "Heat cost allocator"},
    {"num": 9, "name": "Compressed air"},
    {"num": 10, "name": "Cooling (outlet)"},
    {"num": 11, "name": "Cooling (inlet)"},
    {"num": 12, "name": "Heat (inlet)"},
    {"num": 13, "name": "Combined heat/cooling"},
    {"num": 14, "name": "Bus/System component"},
    {"num": 15, "name": "Unknown medium"},
    {"num": 20, "name": "Calorific value"},
    {"num": 21, "name": "Hot water"},
    {"num": 22, "name": "Cold water"},
    {"num": 23, "name": "Dual register (hot/cold) water"},
    {"num": 24, "name": "Pressure"},
    {"num": 25, "name": "A/D Converter"},
    {"num": 26, "name": "Smoke detector"},
    {"num": 27, "name": "Room sensor"},
    {"num": 28, "name": "Gas detector"},
    {"num": 32, "name": "Breaker (electricity)"},
    {"num": 33, "name": "Valve (gas or water)"},
    {"num": 37, "name": "Customer unit"},
    {"num": 40, "name": "Waste water"},
    {"num": 41, "name": "Waste"},
    {"num": 42, "name": "Carbon dioxide"},
    {"num": 49, "name": "Communication controller"},
    {"num": 50, "name": "Unidirectional repeater"},
    {"num": 51, "name": "Bidirectional repeater"},
    {"num": 54, "name": "Radio converter (system side)"},
    {"num": 55, "name": "Radio converter (meter side)"}
]

UNIT_TYPES = [
    {"num": 0, "name": "None", "desc": "None"},
    {"num": 1, "name": "Bin", "desc": "Binary"},
    {"num": 2, "name": "Cur", "desc": "Local currency unit"},
    {"num": 3, "name": "V", "desc": "Volt"},
    {"num": 4, "name": "A", "desc": "Ampere"},
    {"num": 5, "name": "Wh", "desc": "Watt hour"},
    {"num": 6, "name": "J", "desc": "Joule"},
    {"num": 7, "name": "m^3", "desc": "Cubic meter"},
    {"num": 8, "name": "kg", "desc": "Kilogram"},
    {"num": 9, "name": "s", "desc": "Second"},
    {"num": 10, "name": "min", "desc": "Minute"},
    {"num": 11, "name": "h", "desc": "Hour"},
    {"num": 12, "name": "d", "desc": "Day"},
    {"num": 13, "name": "W", "desc": "Watt"},
    {"num": 14, "name": "J/h", "desc": "Joule per hour"},
    {"num": 15, "name": "m^3/h", "desc": "Cubic meter per hour"},
    {"num": 16, "name": "m^3/min", "desc": "Cubic meter per minute"},
    {"num": 17, "name": "m^3/s", "desc": "Cubic meter per second"},
    {"num": 18, "name": "kg/h", "desc": "Kilogram per hour"},
    {"num": 19, "name": "Degree C", "desc": "Degree celsius"},
    {"num": 20, "name": "K", "desc": "Kelvin"},
    {"num": 21, "name": "Bar", "desc": "Bar"},
    {"num": 22, "name": "", "desc": "Dimensionless"},
    {"num": 25, "name": "UTC", "desc": "UTC"},
    {"num": 26, "name": "bd", "desc": "Baud"},
    {"num": 27, "name": "bt", "desc": "Bit time"},
    {"num": 28, "name": "mon", "desc": "Month"},
    {"num": 29, "name": "y", "desc": "Year"},
    {"num": 30, "name": "", "desc": "Day of week"},
    {"num": 31, "name": "dBm", "desc": "dBm"},
    {"num": 32, "name": "Bin", "desc": "Bin"},
    {"num": 33, "name": "Bin", "desc": "Bin"},
    {"num": 34, "name": "kVARh", "desc": "Kilo voltampere reactive hour"},
    {"num": 35, "name": "kVAR", "desc": "Kilo voltampere reactive"},
    {"num": 36, "name": "cal", "desc": "Calorie"},
    {"num": 37, "name": "%", "desc": "Percent"},
    {"num": 38, "name": "ft^3", "desc": "Cubic feet"},
    {"num": 39, "name": "Degree", "desc": "Degree"},
    {"num": 40, "name": "Hz", "desc": "Hertz"},
    {"num": 41, "name": "kBTU", "desc": "Kilo british thermal unit"},
    {"num": 42, "name": "mBTU/s",
        "desc": "Milli british thermal unit per second"},
    {"num": 43, "name": "US gal", "desc": "US gallon"},
    {"num": 44, "name": "US gal/s", "desc": "US gallon per second"},
    {"num": 45, "name": "US gal/min", "desc": "US gallon per minute"},
    {"num": 46, "name": "US gal/h", "desc": "US gallon per hour"},
    {"num": 47, "name": "Degree F", "desc": "Degree Fahrenheit"}
]

REGISTER_TYPES_ARRAY = list(map(lambda item: item.value, RegisterType))
UNIT_TYPES_ARRAY = list(map(lambda item: item["num"], UNIT_TYPES))
MEDIUM_TYPES_ARRAY = list(map(lambda item: item["num"], MEDIUM_TYPES))
METER_TYPES_ARRAY = list(map(lambda item: item.value, MeterFlag))
READABILITY_TYPES_ARRAY = list(map(lambda item: item.value, ReadabilityTypes))
