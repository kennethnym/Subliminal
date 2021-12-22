import asyncio
from .domain import Domain
from .utils import dot
from .request import Request

class DeviceAddedEvent:
    def __init__(self, **kwargs) -> None:
        self.device = Device(**kwargs)


class DeviceRemovedEvent:
    def __init__(self, **kwargs) -> None:
        self.device = Device(**kwargs)


class Device:
    def __init__(self, id: str, name: str, platform: str, category: str, platformType: str, ephemeral: bool, emulator: bool, emulatorId: str) -> None:
        self.id = id
        self.name = name
        self.platform = platform
        self.category = category
        self.platform_type = platformType
        self.ephemeral = ephemeral
        self.emulator = emulator
        self.emulator_id = emulatorId


class DeviceDomain(Domain):
    nsp = "device"

    # device events
    added = dot(nsp, "added")
    removed = dot(nsp, "removed")

    # commands
    __enable = dot(nsp, "enable")
    __disable = dot(nsp, "disable")
    __get_devices = dot(nsp, "getDevices")

    _event_constructor_map = {
        added: DeviceAddedEvent,
        removed: DeviceRemovedEvent,
    }

    _response_constructor_map = {
        __get_devices: Device
    }

    async def enable(self):
        await super().make_request(Request(
            method=self.__enable,
            has_response=False,
        ))


    async def disable(self):
        await super().make_request(Request(
            method=self.__disable,
            has_response=False,
        ))


    async def get_devices(self):
        devices = await super().make_request(Request(
            method=self.__get_devices,
            has_response=True,
        ))
        return devices
