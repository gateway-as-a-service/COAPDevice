import uuid
import sys

from device.libs.utils import get_ip_address

DEVICE_UUID = str(uuid.uuid4())
DEVICE_UUID = "030cd8f1-4334-4643-9c03-1d4d92bcdb61"
DEVICE_INFO = {
    "id": DEVICE_UUID,
    "type": "Thermostat",
    "name": "Bedroom Thermostat",
    "protocol": "COAP",
    "ip": get_ip_address(),
    "port": 5680,
    "unit": "Celsius",
    "u": "C",
    "min": 15,
    "max": 23,
}
DEVICE_INFO["id"] = sys.argv[1]
