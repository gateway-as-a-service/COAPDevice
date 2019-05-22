import json
import socket
import time

from device.configs.config import DISCOVERY_RESPONSE_PORT, DISCOVERY_REQUEST_BROADCAST_PORT
from device.configs.device_info import DEVICE_INFO
from device.libs.utils import FakeLogger


class HubDiscoveryClient(object):

    def __init__(self, device_info, *args, **kwargs):
        self.device_info = device_info
        self.logger = kwargs.get("logger", FakeLogger())
        self.discovery_service_port = kwargs.get("discovery_port", DISCOVERY_REQUEST_BROADCAST_PORT)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.settimeout(5)

    def discover(self):
        binding_address = ("", self.discovery_service_port)
        self.sock.bind(binding_address)

        self.logger.debug("Contacting discovery service")
        while True:
            broadcast_address = ("255.255.255.255", DISCOVERY_RESPONSE_PORT)
            self.sock.sendto(json.dumps(self.device_info).encode("utf-8"), broadcast_address)
            self.logger.debug("Broadcast discovery message for device {}".format(self.device_info["id"]))

            try:
                data, address = self.sock.recvfrom(4096)
            except Exception as err:
                self.logger.info("Timeout for receiving discovery confirmation")
                time.sleep(1)
                continue

            if data != b'OK':
                self.logger.error(data)
                continue

            hub_address = address[0]
            self.logger.debug(
                "Device {} has been registered. Hub's ip {}"
                    .format(self.device_info["id"], hub_address)
            )

            return hub_address


if __name__ == '__main__':
    hub_discovery_client = HubDiscoveryClient(DEVICE_INFO)
    hub_discovery_client.discover()
