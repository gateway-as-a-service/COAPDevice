import json

from coapserver import CoAPServer
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource

from device.configs.device_info import DEVICE_INFO
from device.libs.utils import retrieve_logger


class CoAPSubscriber(Resource):

    def __init__(self, name, device_info):
        super().__init__(name)

        self.device_info = device_info

        self.logger = retrieve_logger("coap_subscriber")

    def render_GET(self, request):
        pass

    def render_GET_advanced(self, request, response):
        pass

    def render_PUT(self, request):
        message = json.loads(request.payload)
        self.logger.info("Received message: {}".format(message))
        self.device_info["value"] = message["value"]
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
