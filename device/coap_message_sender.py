import json

from coapthon.client.helperclient import HelperClient


class CoAPMessageSender(object):
    MAX_ATTEMPTS = 10

    def __init__(self, coap_hostname, coap_port, logger):
        self.coap_client = HelperClient(server=(coap_hostname, coap_port))

        self.logger = logger

    def send_message_put(self, path, data):
        attempts = 0
        while attempts < self.MAX_ATTEMPTS:
            self.logger.info("Attempt {} to send the message to coap microservice".format(attempts))

            response = self.coap_client.put(path, json.dumps(data), timeout=10)
            self.logger.info("Response: {}".format(response))
            if response:
                self.logger.info(
                    "Successfully sent the message {} to coap microservice at path {}".format(data, path)
                )
                return True

            self.logger.warning("Failed to retrieve response from CoAP microservice. Try again")
            attempts += 1

        self.logger.error("Failed to send the message to the coap microservice")
        return False
