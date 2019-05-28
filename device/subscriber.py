import json

from coapthon.resources.resource import Resource
from coapthon.server.coap import CoAP

from device.coap_message_sender import CoAPMessageSender
from device.configs.device_info import DEVICE_INFO
from device.libs.utils import retrieve_logger


class CoAPSubscriber(Resource):
    COAP_SERVER_HUB_PORT = 5683
    COAP_SERVER_HUB_PATH = "devices"

    MAX_ATTEMPTS = 5

    def __init__(self, name, device_info, hub_address="10.0.75.1"):  # TODO: Remove this hardcode for hub_address
        super().__init__(name)

        self.device_info = device_info

        self.logger = retrieve_logger("coap_subscriber")

        self.hub_address = hub_address
        self.coap_sender_message = CoAPMessageSender(self.hub_address, self.COAP_SERVER_HUB_PORT, self.logger)

    def render_GET(self, request):
        pass

    def render_GET_advanced(self, request, response):
        pass

    def render_PUT(self, request):
        received_message = json.loads(request.payload)
        self.logger.info("Received message: {}".format(received_message))
        self.device_info["value"] = received_message["value"]

        message_to_send_to_gateway = {
            "id": self.device_info["id"],
            "n": self.device_info["name"],
            "v": received_message["value"],
            "u": self.device_info["u"],
        }
        self.logger.info(
            "Send message {} to the coap micro-service at path: {}"
                .format(message_to_send_to_gateway, self.COAP_SERVER_HUB_PATH)
        )
        self.coap_sender_message.send_message_put(self.COAP_SERVER_HUB_PATH, message_to_send_to_gateway)

        return self

    def render_PUT_advanced(self, request, response):
        pass

    def render_POST(self, request):
        pass

    def render_POST_advanced(self, request, response):
        pass

    def render_DELETE(self, request):
        pass

    def render_DELETE_advanced(self, request, response):
        pass


class CoAPDeviceServer(CoAP):
    def __init__(self, host, port, device_info):
        super().__init__((host, port))
        device_coap_path = "devices-{}".format(device_info["id"])
        print("Add Resource for path {}".format(device_coap_path))
        self.add_resource(device_coap_path, CoAPSubscriber("CoAPSubscriber", device_info))


def _start_server():
    server = CoAPDeviceServer("0.0.0.0", DEVICE_INFO["port"], DEVICE_INFO)
    try:
        server.listen(10)
    except KeyboardInterrupt:
        print("Server Shutdown")
        server.close()
        print("Closing....")


if __name__ == '__main__':
    _start_server()
