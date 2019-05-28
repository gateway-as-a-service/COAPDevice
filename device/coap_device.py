import random
import time

from device.coap_message_sender import CoAPMessageSender
from device.configs.device_info import DEVICE_INFO
from device.discovery_client import HubDiscoveryClient
from device.libs.utils import retrieve_logger


class COAPSmartObject(object):
    COAP_SERVER_HUB_PORT = 5683
    COAP_SERVER_HUB_PATH = "devices"
    SLEEP_PERIOD = 60

    def __init__(self, device_info, *args, **kwargs):
        self.device_info = device_info
        self.coap_message_sender = None

        self.logger = retrieve_logger("coap_device")

    def _discover_hub(self):
        hub_discovery_client = HubDiscoveryClient(self.device_info, logger=self.logger)
        hub_address = hub_discovery_client.discover()
        self.coap_message_sender = CoAPMessageSender(hub_address, self.COAP_SERVER_HUB_PORT, self.logger)

    def start(self):
        self._discover_hub()

        while True:
            data = {
                "id": self.device_info["id"],
                "n": self.device_info["name"],
                "v": random.randint(self.device_info["min"], self.device_info["max"]),
                "u": self.device_info["u"],
            }
            self.logger.info(
                "Send the message {} to coap micro-service at path: {}".format(data, self.COAP_SERVER_HUB_PATH)
            )

            self.coap_message_sender.send_message_put(self.COAP_SERVER_HUB_PATH, data)

            self.logger.info("Sleeping.....")
            time.sleep(self.SLEEP_PERIOD)


if __name__ == '__main__':
    coap_smart_object = COAPSmartObject(DEVICE_INFO)
    coap_smart_object.start()
