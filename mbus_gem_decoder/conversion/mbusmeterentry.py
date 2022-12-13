"""Convert raw data to METER ENTRY type
"""

__version__ = "0.1.0"
__author__ = "René"

import json
from . import READABILITY_TYPES_ARRAY
from . import get_integer_value, get_float_value, get_scale, get_unit
from . import register_type, register_type_str, get_unit_type
from . import get_unix_timestamp, get_timestamp


class MBusMeterEntry:
    """MBUS-GEM METER ENTRY class
    """
    def __init__(
                 self,
                 ten_regs: list[int],
                 gw_reg: int,
                 human: int = 0) -> None:
        """Constructor

        Args:
            ten_regs (list[int]): Ten register values as list of integers.
            gw_reg (int): Register as declared in the MBUS-GEM gateway.
            human (int, optional): Generate human readable values: 0 -- ignore,
            1 -- only human readable values, 2 -- both. Defaults to 0.
        """

        if gw_reg < 0:
            raise Exception("Gateway register cannot be negative")
        if len(ten_regs) != 10:
            raise Exception("Must provide exactly ten register values")
        # if human not in [0, 1, 2]:
        if human not in READABILITY_TYPES_ARRAY:
            raise Exception("Illegal value for human readability")
        self.ten_regs = ten_regs
        self.gw_reg = gw_reg
        self.human = human
        self.convert_data_in_regsmeter_entry()

    def convert_data_in_regsmeter_entry(self) -> object:
        """Convert registers that hold data about a METER ENTRY.

        Get data/info about specific value of meter.

        Returns:
            object: Object of human-readable data

        |REG| VALUE          |SIZE  | DETAILS                                 |
        |:--|:---------------|-----:|:----------------------------------------|
        |0-3| Meter value    | 64bit| Signed integer (not scaled)             |
        |4-5| Meter value    | 32bit| Floating point value (scaled)           |
        |6  | Scale factor   | 16bit| Signed scale factor (power of 10)       |
        |7  | Type/Unit      | 16bit| Type field set in the upper byte; Unit  |
        |   |                |      | in the lower byte                       |
        |8-9| Time stamp     | 32bit| Unix time stamp                         |
        """

        self.reg = self.gw_reg
        self.integer = get_integer_value(self.ten_regs)
        self.scale = get_scale(self.ten_regs)
        self.float = get_float_value(self.ten_regs)
        self.unit = get_unit(self.ten_regs)
        self.unix_timestamp = get_unix_timestamp(self.ten_regs)
        self.register_type = register_type(self.ten_regs)

    def to_object(self) -> object:
        """Convert to object

        Returns:
            object: data as object
        """
        data = {}
        data["reg"] = self.reg
        data["integer"] = self.integer
        data["scale"] = self.scale
        data["float"] = self.float
        if self.human in [0, 2]:
            data["unit"] = self.unit
            data["timestampUnix"] = self.unix_timestamp
            data["type"] = self.register_type
        if self.human in [1, 2]:
            unit_readable = get_unit_type(self.unit)
            data["unit_string"] = unit_readable["name"]
            data["unit_description"] = unit_readable["desc"]
            data["timestamp"] = get_timestamp(self.ten_regs)
            data["type_string"] = register_type_str(self.ten_regs)
        return data

    def __str__(self):
        data = self.to_object()
        return json.dumps(data)
