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
PlateType = Annotated[Literal["corning_96_wellplate_360ul_flat"], "value should be in the list"]


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
        slot: SLOT,
    ) -> protocol_api.labware.Labware:
        return self.protocol.load_labware(tiprack_type, slot)

    def load_plate(
            self,
            plate_type
    )