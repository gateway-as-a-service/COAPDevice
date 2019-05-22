import json
import random

import time

from device.configs.device_info import DEVICE_INFO
from device.discovery_client import HubDiscoveryClient
from device.libs.utils import retrieve_logger

from coapthon.client.helperclient import HelperClient


class COAPSmartObject(object):
    COAP_SERVER_HUB_PORT = 5683
    COAP_SERVER_HUB_PATH = "devices"
    SLEEP_PERIOD = 10

    def __init__(self, device_info, *args, **kwargs):
        self.device_info = device_info
        self.hub_address = None
        self.coap_client = None

        self.logger = retrieve_logger("coap_device")

    def _discover_hub(self):
        hub_discovery_client = HubDiscoveryClient(self.device_info, logger=self.logger)
        hub_address = hub_discovery_client.discover()
        self.hub_address = hub_address
        self.coap_client = HelperClient(server=(self.hub_address, self.COAP_SERVER_HUB_PORT))

    def _send_message(self, message):
        pass

    def start(self):
        self._discover_hub()

        while True:
            data = {
                "id": self.device_info["id"],
                "n": self.device_info["name"],
                "v": random.randint(self.device_info["min"], self.device_info["max"]),
                "u": self.device_info["u"],
            }
            response = self.coap_client.put(self.COAP_SERVER_HUB_PATH, json.dumps(data))
            if response:
                self.logger.info("Response message: {}".format(response))
            else:
                self.logger.warning("Failed to retrieve the response from Gateway")

            self.logger.info("Sleeping.....")
            time.sleep(self.SLEEP_PERIOD)


if __name__ == '__main__':
    coap_smart_object = COAPSmartObject(DEVICE_INFO)
    coap_smart_object.start()
