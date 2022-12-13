"""MBUS-GEM

Package for decoding MBUS-GEM register data into JSON format, optionally in
more verbose human-readable values. The decoder takes a list of ten integers
and converts it to a JSON object based on the object type:

*MBUS-GEM (gateway)
*METER
*METER ENTRY

Author: René
Version: 0.1.0
Copyright: GPLv3

Date: 2022-11-8
"""


__version__ = "0.1.0"
__author__ = "René"

from . import RegisterType, REGISTER_TYPES_ARRAY, READABILITY_TYPES_ARRAY
from . import MBusMeter, MBusMeterEntry, MBusMBus


class MBusDecode:
    """MBUS-GEM class for decoding data from MBUS-GEM gateway's registers.
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
        self.conversion = None
        reg_type = abs(self.ten_regs[7] >> 8)
        if reg_type in REGISTER_TYPES_ARRAY:
            if reg_type == RegisterType.METER_ENTRY.value:
                self.conversion = MBusMeterEntry(
                    self.ten_regs, self.gw_reg, self.human)
            elif reg_type == RegisterType.METER.value:
                self.conversion = MBusMeter(
                    self.ten_regs, self.gw_reg, self.human)
            elif reg_type == RegisterType.MBUS_GEM.value:
                self.conversion = MBusMBus(
                    self.ten_regs, self.gw_reg, self.human)
            else:
                raise Exception("Illegal register type")
        else:
            raise Exception("Illegal register type")

            # self.conversion = switch_.get(
            #     RegisterType(abs(self.ten_regs[7] >> 8)), {})

    def __str__(self) -> str:
        if isinstance(self.conversion, type(None)):
            raise Exception("Conversion failed")
        return str(self.conversion)

    def to_object(self) -> object:
        """Convert class to object

        Raises:
            Exception: Conversion has failed

        Returns:
            object: Converted object
        """

        if isinstance(self.conversion, type(None)):
            raise Exception("Conversion failed")
        return self.conversion.to_object()
