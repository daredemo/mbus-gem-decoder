"""Test reading MBUS-GEN data over TCP.
"""

__version__ = "0.0.1"
__author__ = "René Pihlak"

import time
import json
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
# import pandas as pd

from pyModbusTCP.client import ModbusClient
# from pyModbusTCP import utils

# from mbus.mbusgem import MBusGem
# from mbusgemdecoder import *
from mbus_gem_decoder import MBusDecode

HOSTNAME = "localhost"
HOSTPORT = 9090

ERROR_EMPTY_REQUEST = {'error': 'Empty request'}
ERROR_DEVICE = {'error': 'Device error'}
ERROR_IP = {'error': 'Cannot connect to IP address'}
ERROR_PORT = {'error': 'Cannot connect to port'}

# MBUS_SERVER_IP = '192.168.120.123'
# MBUS_SERVER_PORT = 502

# MG = MBusGem()
# connection_.close()


def is_port_open(ip_address: str, port: str, udp: bool = True) -> bool:
    """Check if a port is open.

    Args:
        ip (str): IP address
        port (str): Port number
        udp (bool): Protocol (True -> UDP, False -> TCP)

    Returns:
        bool: Is port open?
    """
    a_socket = None
    if udp:
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(2.0)  # seconds (float)

    location = (ip_address, int(port))
    check = a_socket.connect_ex(location)
    try:
        a_socket.close()
    except socket.error:
        print(socket.error)
    return check == 0


def is_valid_ipv4_address(address: str) -> bool:
    """Validate IPv4 address.

    Args:
        address (str): IP address.

    Returns:
        bool: Is valid?
    """
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True


class MBusGemPostServer(BaseHTTPRequestHandler):
    """Server class
    """

    def send_custom_header(self, code: int = 200) -> None:
        """Set HTTP responce status code and send headers

        Args:
            code (int, optional): HTTP responce status code. Defaults to 200.
        """
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header(
            'Cache-Control', 'private, no-cache, no-store, must-revalidate')
        self.send_header('Expires', '-1')
        self.send_header('Pragma', 'no-cache')
        self.end_headers()

    def do_POST(self) -> None:
        """POST method respose.
        """
        connection_ = None
        content_length = -1
        data_out = None
        if 'content-length' in self.headers:
            content_length = int(self.headers['content-length'])
        if content_length > 0:
            content_json = json.loads(
                self.rfile.read(content_length).decode('utf-8'))
            try:
                if is_valid_ipv4_address(content_json["controller_ip"]):
                    if is_port_open(
                      content_json["controller_ip"],
                      content_json["controller_port"],
                      False):
                        controller_ip = content_json["controller_ip"]
                        controller_registers = content_json[
                          "controller_registers"]
                        controller_port = content_json["controller_port"]
                        connection_ = ModbusClient(
                            host=controller_ip,
                            port=int(controller_port),
                            auto_open=True
                        )
                        data_out = self.get_readings(
                            connection_,
                            controller_ip,
                            controller_port,
                            controller_registers)
                    else:
                        data_out = ERROR_PORT
                else:
                    data_out = ERROR_PORT
            except Exception as device_exception:
                print(repr(device_exception))
                data_out = ERROR_DEVICE
            finally:
                if not isinstance(connection_, type(None)):
                    connection_.close()
        else:
            data_out = ERROR_EMPTY_REQUEST
        # Send response
        if data_out == ERROR_DEVICE:
            self.send_custom_header(500)
        elif data_out == ERROR_EMPTY_REQUEST:
            self.send_custom_header(400)
        elif (data_out == ERROR_PORT) or (data_out == ERROR_IP):
            self.send_custom_header(404)
        elif len(data_out["data"]) == 0:
            data_out = ERROR_DEVICE
            self.send_custom_header(400)
        else:
            self.send_custom_header()
        self.wfile.write(bytes(json.dumps(data_out), "utf-8"))

    def get_readings(
            self,
            controller,
            controller_ip,
            controller_port,
            controller_registers):
        """Get data from MBUS-GEM device.

        Args:
            controller (MBUS device): Controller instance.
            controller_ip (str): IP address of the controller.
            controller_port (str): Port of the controller.
            controller_registers (list(int)): List of registers to read.

        Returns:
            (JSON Object): Meter data as a list of JSON Objects.
        """
        data_object = {"ip": controller_ip,
                       "registers": list(map(int, controller_registers)),
                       "port": controller_port,
                       "type": "MBUS GEM",
                       "data": []}
        value_objects = {}
        for each_ in list(map(int, controller_registers)):
            data_from_meter = controller.read_holding_registers(
                each_, 10)
            if data_from_meter:
                try:
                    value_point = {}
                    value_point = MBusDecode(
                        data_from_meter,
                        each_, 2).to_object()
                    if value_point:
                        value_objects[each_] = value_point
                except Exception as error:
                    print(repr(error))
        data_object["data"] = value_objects
        return data_object


if __name__ == '__main__':
    mbus_gem_server = HTTPServer((HOSTNAME, HOSTPORT), MBusGemPostServer)
    print(time.asctime(), f"Server starts - {HOSTNAME}:{HOSTPORT}")

    try:
        mbus_gem_server.serve_forever()
    except KeyboardInterrupt:
        pass

    mbus_gem_server.server_close()
    print(time.asctime(), f"Server stops - {HOSTNAME}:{HOSTPORT}")
