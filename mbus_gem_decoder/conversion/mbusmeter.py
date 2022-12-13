"""Convert raw data to METER type
"""

__version__ = "0.1.0"
__author__ = "René"

import json
from . import READABILITY_TYPES_ARRAY
from . import meter_serial, meter_manufacturer, meter_version, meter_medium
from . import meter_medium_str, meter_flag1, meter_flag2, meter_flag1_str
from . import meter_flag2_str, register_type, register_type_str
from . import get_unix_timestamp, get_timestamp


class MBusMeter:
    """MBUS-GEM METER class
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
        self.convert_data_in_regsmeter()

    def convert_data_in_regsmeter(self) -> object:
        """Convert registers that hold data about a METER.

        Returns:
            object: Object with human-readable data

        |REG| VALUE          |SIZE  | DETAILS                                 |
        |:--|:---------------|-----:|:----------------------------------------|
        |0-1| Serial number  | 32bit| Serial number of meter as integer value |
        |2  | Manufacturer ID| 16bit| Encoding of manufacturer by using       |
        |   |                |      | different blocks of bits:               |
        |   |                |      | 10-14, 1st; 5-9, 2nd; 0-4, 3rd (A=1)    |
        |3  | Version/Medium | 16bit| Version of meter: upper byte; Medium:   |
        |   |                |      | lower byte                              |
        |4-5| Time stamp     | 32bit| Unix time stamp of last read-out        |
        |6  | Reserved       | 16bit|                                         |
        |7  | Type field     | 16bit| Type field for register set in the upper|
        |   |                |      | byte, lower byte is reserved            |
        |8  | Flags/Reserved | 16bit| bit[0]=1: meter could not be read;      |
        |   |                |      | bit[0]=0: could be read correctly;      |
        |   |                |      | bit[1]=1: not all values are updated;   |
        |   |                |      | bit[1]=0: all meter values updated;     |
        |   |                |      | bit[2:15] reserved;                     |
        |9  | Reserved       | 16bit|                                         |
        """

        self.reg = self.gw_reg
        self.serial = meter_serial(self.ten_regs)
        self.manufacturer = meter_manufacturer(self.ten_regs)
        self.version = meter_version(self.ten_regs)
        self.medium = meter_medium(self.ten_regs)
        self.unix_timestamp = get_unix_timestamp(self.ten_regs)
        self.flag1 = meter_flag1(self.ten_regs)
        self.flag2 = meter_flag2(self.ten_regs)
        self.register_type = register_type(self.ten_regs)

    def to_object(self) -> object:
        """Convert to object

        Returns:
            object: data as object
        """
        data = {}
        data["reg"] = self.reg
        data["serialNo"] = self.serial
        data["manufacturerID"] = self.manufacturer
        data["version"] = self.version
        if self.human in [0, 2]:
            data["medium"] = self.medium
            data["timestampUnix"] = self.unix_timestamp
            data["flag1"] = self.flag1
            data["flag2"] = self.flag2
            data["type"] = self.register_type
        if self.human in [1, 2]:
            data["medium_string"] = meter_medium_str(self.medium)
            data["timestamp"] = get_timestamp(self.ten_regs)
            data["flag1_string"] = meter_flag1_str(self.ten_regs)
            data["flag2_string"] = meter_flag2_str(self.ten_regs)
            data["type_string"] = register_type_str(self.ten_regs)
        return data

    def __str__(self):
        data = self.to_object()
        return json.dumps(data)
