import sys
import subprocess
import random

DEVICES_UUIDS = [
    '017c257b-01da-48e5-b8e4-e3b2d2f1797b', 'b5c406c8-9d1e-491e-aaeb-a6971dd05135',
    'c04bdd1e-8e8f-4852-8088-cfa97196031d', 'edd4e981-7155-41ad-8a0f-da4ff8f25033',
    'adb6c602-43fb-41b4-8c9a-834fd1fcf646', 'ba80f391-df1d-4164-9686-240fa8733ec2',
    '8a52d240-ebcc-4a5a-82aa-c16879ac136c', '4d364d23-3d3c-4e9a-ab68-67dbe9cebf9b',
    'b07a0931-5a2b-4a9e-83a9-546c6f55fab3', '1ebed9e6-c948-4bc3-8065-e86aff2f7df4',
    'b2b9cd9e-1b6b-422a-9475-760684ef8caa', '178a4756-bc30-4266-ba4c-cf861fec14c6',
    '1eaa0a19-48e8-447d-a10d-76af3fe44532', '22eecd76-dfbe-49a5-970a-75d7b88a513c',
    '8ae3d31b-e095-46b5-808d-3b9f88fd2f0e', '1a642569-409c-4f02-b54b-8cc3f43ffbc4',
    'fa5f86ad-3f8a-4202-9eab-f1cbc2766c3b', '55608f1e-5d26-43e6-8d71-f8bf9d3dbb5e',
    '8bb75926-65f2-4d13-a187-333384507958', '0bfa5246-4346-405f-bcb2-ad30cb4d4211',
]

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception("Must provide the number of devices")

    number_of_devices = int(sys.argv[1])
    selected_devices_uuids = random.sample(DEVICES_UUIDS, number_of_devices)
    for device_uuid in selected_devices_uuids:
        device_command = [
            r"E:\VirtualEnvs\Python3\COAP_Device\Scripts\python.exe", "./coap_device.py", device_uuid
        ]

        subprocess.Popen(device_command, shell=False)

        # receiver_command = ["start", r"E:\VirtualEnvs\Python3\MQTT_Device\Scripts\python.exe", "./receiver.py",
        #                     device_uuid]
        # subprocess.Popen(receiver_command, shell=True)
