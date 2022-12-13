"""Helper methods
"""

__version__ = "0.1.0"
__author__ = "René"


import struct
from datetime import datetime

from .mbustypes import MEDIUM_TYPES_ARRAY, MEDIUM_TYPES
from .mbustypes import UNIT_TYPES_ARRAY, UNIT_TYPES
from .mbustypes import REGISTER_TYPES_ARRAY, RegisterType
from .mbustypes import MeterFlag


def meter_serial(ten_regs: list[int]) -> str:
    """Convert METER's serial number

    Args:
        ten_regs (list[int]): registers

    Returns:
        str: serial number
    """

    return f"{((ten_regs[0] << 16) + ten_regs[1]):08d}"


def meter_manufacturer(ten_regs: list[int]) -> str:
    """Convert a numeric manufacturer code to string/letters.

    Args:
        ten_regs (list[int]): registers

    Returns:
        str: Three letter code of manufacturer
    """

    reg = ten_regs[2]
    id_1 = chr(ord("A") + ((reg >> 10) & 0x1F) - 1)
    id_2 = chr(ord("A") + ((reg >> 5) & 0x1F) - 1)
    id_3 = chr(ord("A") + (reg & 0x1F) - 1)
    return f"{id_1}{id_2}{id_3}"


def meter_version(ten_regs: list[int]) -> int:
    """Convert METER's version to integer value

    Args:
        ten_regs (list[int]): registers

    Returns:
        int: version number
    """

    return ten_regs[3] >> 8


def meter_medium(ten_regs: list[int]) -> int:
    """METER's medium

    Args:
        ten_regs (list[int]): registers

    Returns:
        int: medium
    """

    return ten_regs[3] & 0xFF


def meter_medium_str(value: int = -1) -> str:
    """Convert numeric medium type to string.

    Args:
        value (int): Numeric medium type. Defaults to -1.

    Returns:
        str: Medium type as a string
    """

    if value in MEDIUM_TYPES_ARRAY:
        return list(
            filter(
                lambda x: x["num"] == value,
                MEDIUM_TYPES))[0]["name"]
    if value < 0 or value > 255:
        raise Exception("Medium index is out of range")
    return "Reserved"


def meter_flag1(ten_regs: list[int]) -> int:
    """Get METER's flag1 as integer

    Args:
        ten_regs (list[int]): registers

    Returns:
        int: flag1
    """

    return ten_regs[8] & 0x01


def meter_flag1_str(ten_regs: list[int]) -> str:
    """Get METER's flag1 as string

    Args:
        ten_regs (list[int]): registers

    Returns:
        str: flag1
    """

    return MeterFlag(ten_regs[8] & 0x01).name


def meter_flag2(ten_regs: list[int]) -> int:
    """Get METER's flag2 as integer

    Args:
        ten_regs (list[int]): registers

    Returns:
        int: flag2
    """

    return ((ten_regs[8] >> 1) & 0x01) + 2


def meter_flag2_str(ten_regs: list[int]) -> str:
    """Get METER's flag2 as string

    Args:
        ten_regs (list[int]): registers

    Returns:
        str: flag2
    """

    return MeterFlag(((ten_regs[8] >> 1) & 0x01) + 2).name


def register_type(ten_regs: list[int]) -> int:
    """METER's type as integer

    Args:
        ten_regs (list[int]): registers

    Returns:
        int: type
    """

    register_type_value = abs(ten_regs[7] >> 8)
    if register_type_value not in REGISTER_TYPES_ARRAY:
        raise Exception("Register type value out of range")
    return register_type_value


def register_type_str(ten_regs: list[int]) -> str:
    """METER's type as string

    Args:
        ten_regs (list[int]): registers

    Returns:
        str: type
    """

    register_type_value = abs(ten_regs[7] >> 8)
    if register_type_value not in REGISTER_TYPES_ARRAY:
        raise Exception("Register type value out of range")
    return RegisterType(register_type_value).name


def get_sign_correction(ten_regs: list[int]) -> int:
    """Get sign correction value

    Args:
        ten_regs (list[int]): registers

    Returns:
        int: sign correction  (1 or -1)
    """

    return -1 if (ten_regs[0] >> 15) & 0x01 else 1


def get_integer_value(ten_regs: list[int]) -> int:
    """Get integer value of the reading.

    Args:
        ten_regs (list[int]): List of four (4) 16-bit integer values

    Returns:
        int: 64-bit integer value
    """

    sign_correction = get_sign_correction(ten_regs)
    raw_value = (ten_regs[0] & 0x3FFF) << 16
    raw_value = (raw_value + ten_regs[1]) << 16
    raw_value = (raw_value + ten_regs[2]) << 16
    raw_value = raw_value + ten_regs[3]
    return abs(sign_correction * raw_value) * sign_correction


def get_scale(ten_regs: list[int]) -> int:
    """Scaling factor

    Args:
        ten_regs (list[int]): registers

    Returns:
        int: scaling factor

    \f[float \approx integer\times 10^{scale}\f]
    """

    correction = -1 if (ten_regs[6] >> 15) & 0x01 else 1
    return abs((correction * ten_regs[6]) & 0x7FFF) * correction


def get_float_value(ten_regs: list[int]) -> float:
    """Get floating point value

    Args:
        ten_regs (list[int]): registers

    Returns:
        float: approximate floating point value
    """

    return two_words_to_ieee(ten_regs[4], ten_regs[5])


def int32_to_ieee(val_int: int) -> float:
    """Convert Python int32 to IEEE float.

    Args:
        val_int (int): Value to convert to float

    Returns:
        float: Converted value as an IEEE floating point
    """

    return struct.unpack("f", struct.pack("I", val_int))[0]


def two_words_to_ieee(val_one: int, val_two: int) -> float:
    """Convert two words (16 bit) to IEEE float (32 bit).

    Args:
        val_one (int): The first value (16 bit)
        val_two (int): The second value (16 bit)

    Returns:
        float: Combined IEEE float (32 bit)
    """

    val_int32 = two_words_to_long(val_one, val_two)
    return int32_to_ieee(val_int32)


def two_words_to_long(val_one: int, val_two: int) -> int:
    """Convert two words (16 bit) to long (32 bit).

    Args:
        val_one (int): The first value (16 bit)
        val_two (int): The second value (16 bit)

    Returns:
        int: Combined long (32 bit)
    """

    return (val_one << 16) + val_two


def get_unit(ten_regs: list[int]) -> int:
    """Unit of measure

    Args:
        ten_regs (list[int]): registers

    Returns:
        int: Unit of measure
    """

    return ten_regs[7] & 0xFF


def get_unit_type(value: int) -> dict[str, str]:
    """Convert numeric unit type to string.

    Args:
        value (int): Numeric unit type

    Returns:
        dict[str, str]: Unit type as a dictionary of strings
        (name (short form), desc (description or full form of the unit))
    """

    if value in UNIT_TYPES_ARRAY:
        unit_match = list(
            filter(
                lambda x: x["num"] == value, UNIT_TYPES))
        return list(
            map(
                lambda x:
                {
                    "name": x["name"],
                    "desc": x["desc"]
                }, unit_match))[0]
    if value < 0 or value > 255:
        raise Exception("Unit value out of range")
    return {"name": "Res", "desc": "Reserved"}


def mbus_serial(ten_regs: list[int]) -> str:
    """Get serial number of MBUS-GEM gateway

    Args:
        ten_regs (list[int]): registesr

    Returns:
        str: serial number
    """

    return f"{ten_regs[0]:04X}{ten_regs[1]:04X}"


def mbus_protocol_version(ten_regs: list[int]) -> int:
    """Protocol version

    Args:
        ten_regs (list[int]): registers

    Returns:
        int: Protocol version
    """

    return ten_regs[2]


def mbus_version(ten_regs: list[int]) -> str:
    """Protocol version

    Args:
        ten_regs (list[int]): registers

    Returns:
        str: Protocol version
    """

    return f"{ten_regs[3]//100}.{ten_regs[3]%100}"


def get_unix_timestamp(ten_regs: list[int]) -> int:
    """UNIX timestamp

    Args:
        ten_regs (list[int]): registers

    Returns:
        int: UNIX timestamp
    """

    return (ten_regs[4] << 16) + ten_regs[5]


def get_timestamp(ten_regs: list[int]) -> str:
    """Timestamp

    Args:
        ten_regs (list[int]): registers

    Returns:
        str: Timestamp
    """

    unix_time = get_unix_timestamp(ten_regs)
    return datetime.utcfromtimestamp(unix_time).strftime("%Y-%m-%d %H:%M:%S")
