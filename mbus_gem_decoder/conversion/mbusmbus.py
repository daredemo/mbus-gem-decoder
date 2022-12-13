"""Convert raw data to MBUS-GEM gateway type
"""

__version__ = "0.1.0"
__author__ = "René"

import json
from . import READABILITY_TYPES_ARRAY
from . import mbus_serial, mbus_protocol_version, mbus_version
from . import register_type, register_type_str
from . import get_unix_timestamp, get_timestamp


class MBusMBus:
    """MBUS-GEM gateway class
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
        self.convert_data_in_regs_mbusgem()

    def convert_data_in_regs_mbusgem(self) -> object:
        """Convert registers that hold data about the MBUS-GEM gateway.

        Returns:
            object: Object with human-readable data

        |REG| VALUE          |SIZE  | DETAILS                                 |
        |:--|:---------------|-----:|:----------------------------------------|
        |0-1|Serial number   | 32bit| Serial number of MBUS-GEM as hexadecimal|
        |   |                |      | number                                  |
        |2  |Protocol version| 16bit| Protocol version for ModBus interface   |
        |   |                |      | (value=1)                               |
        |3  |Version         | 16bit| Software version of the gateway (as     |
        |   |                |      | integer)                                |
        |4-5|Time stamp      | 32bit| Unix time stamp of last read-out        |
        |6  |Reserved        | 16bit|                                         |
        |7  |Type field      | 16bit| Type field for register set in the upper|
        |   |                |      | byte, lower byte is reserved            |
        |8-9| Reserved       | 32bit|                                         |
        """

        self.reg = self.gw_reg
        self.serial = mbus_serial(self.ten_regs)
        self.protocol = mbus_protocol_version(self.ten_regs)
        self.version = mbus_version(self.ten_regs)
        self.unix_timestamp = get_unix_timestamp(self.ten_regs)
        self.register_type = register_type(self.ten_regs)

    def to_object(self) -> object:
        """Convert to object

        Returns:
            object: data as object
        """
        data = {}
        data["reg"] = self.reg
        data["serialNo"] = self.serial
        data["protocolVersion"] = self.protocol
        data["version"] = self.version
        if self.human in [0, 2]:
            data["timestampUnix"] = self.unix_timestamp
            data["type"] = self.register_type
        if self.human in [1, 2]:
            data["timestamp"] = get_timestamp(self.ten_regs)
            data["type_string"] = register_type_str(self.ten_regs)
        return data

    def __str__(self):
        data = self.to_object()
        return json.dumps(data)
