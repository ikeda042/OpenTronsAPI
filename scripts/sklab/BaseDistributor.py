from opentrons import protocol_api
from typing import Literal
import requests
from datetime import datetime, timedelta, timezone
from typing import Annotated

Jst: timezone = timezone(timedelta(hours=+9))
Slot = Annotated[
    Literal["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
    "value should be between 1 and 12",
]
PlateType = Annotated[
    Literal["corning_96_wellplate_360ul_flat"], "value should be in the list"
]
PipetteType = Annotated[
    Literal["p300_multi_gen2", "p20_multi_gen2"], "value should be in the list"
]
Mount = Annotated[Literal["left", "right"], "value should be in the list"]


metadata = {
    "protocolName": "Base Distributor",
    "author": "ikeda042",
    "description": "分注プロトコル(リザーバーから)",
    "apiLevel": "2.18",
}


class LabwareLoader:
    def __init__(self, protocol: protocol_api.ProtocolContext) -> None:
        self.protocol = protocol

    def get_tiprack(
        self,
        tiprack_type: Literal[
            "opentrons_96_tiprack_300ul", "opentrons_96_tiprack_20ul"
        ],
        slot: Slot,
    ) -> protocol_api.labware.Labware:
        return self.protocol.load_labware(tiprack_type, slot)

    def load_plate(
        self,
        plate_type: PlateType,
        slot: Slot,
    ) -> protocol_api.labware.Labware:
        return self.protocol.load_labware(plate_type, slot)

    def load_pipette(
        self,
        pipette_type: Literal["p300_multi_gen2", "p20_multi_gen2"],
        tiprack: protocol_api.labware.Labware,
        mount: Mount,
    ) -> protocol_api.InstrumentContext:
        return self.protocol.load_instrument(pipette_type, mount, tip_racks=[tiprack])


class BaseDistributor:
    def __init__(self, protocol: protocol_api.ProtocolContext) -> None:
        self.protocol: protocol_api.ProtocolContext = protocol
        labware_loader: LabwareLoader = LabwareLoader(protocol)
        self.tiprack: protocol_api.labware.Labware = labware_loader.get_tiprack(
            "opentrons_96_tiprack_300ul", "1"
        )
