import asyncio
from bleak import BleakScanner
from bleak import BleakClient
from enum import Enum
# Network node service uuid
network_node_service = '680c21d9-c946-4c1f-9c11-baa1c21329e7'


class Ble_Network(Enum):

    # Network node characteristics
    operation_mode = '3f0afd88-7770-46b0-b5e7-9fc099598964'
    network_id = '80f9d8bc-3bff-45bb-a181-2d6a37991208'
    location_data_mode = 'a02b947e-df97-4516-996a-1882521e0ead'
    location_data = '003bbdf2-c634-4b3d-ab56-7ec889b89a37'
    proxy_positions = 'f4a67d7d-379d-4183-9c03-4b6ea5103291'
    device_info = '1e63b1eb-d4ed-444e-af54-c1e965192501'
    statistics = '0eb2bc59-baf1-4c1c-8535-8a0204c69de5'


class Ble_Anchor(Enum):
    # Anchor-specific characteristics
    persisted_position = 'f0f26c9b-2c8c-49ac-ab60-fe03def1b40c'
    mac_stats = '28d01d60-89d3-4bfa-b6e9-651ba596232c'
    cluster_info = '17b1613e-98f2-4436-bcde-23af17a10c72'
    anchor_list = '5b10c428-af2f-486f-aee1-9dbd79b6bccb'


class Ble_Tag(Enum):
    # Tag-specific characteristics
    update_rate = '7bd47f30-5602-4389-b069-8305731308b6'


dw_devices = []


async def scan():
    scanner = BleakScanner()
    devices = await scanner.discover()
    for d in devices:
        if d.name[0:2] == 'DW':
            print(d.name)
            dw_devices.append({"name": d.name, "address": d.address})


async def init(address):
    async with BleakClient(address) as client:
        for c_str in Ble_Network:
            data = await client.read_gatt_char(c_str.value)
            print(c_str.name)
            print(data)

loop = asyncio.get_event_loop()
loop.run_until_complete(scan())
for d in dw_devices:
    loop.run_until_complete(init(d["address"]))
