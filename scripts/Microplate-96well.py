from opentrons import protocol_api
from typing import Literal
import requests
from datetime import datetime, timedelta, timezone

JST: timezone = timezone(timedelta(hours=+9))

metadata = {
    "protocolName": "Microplate 96-well Protocol",
    "author": "ikeda042",
    "description": "Basic Protocol for testing",
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
        slot: Literal["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
    ) -> protocol_api.labware.Labware:
        return self.protocol.load_labware(tiprack_type, slot)

    def load_plate(
        self,
        plate_type: Literal["corning_96_wellplate_360ul_flat"],
        slot: Literal["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
    ) -> protocol_api.labware.Labware:
        return self.protocol.load_labware(plate_type, slot)

    def load_pipette(
        self,
        pipette_type: Literal["p300_multi_gen2", "p20_multi_gen2"],
        tiprack: protocol_api.labware.Labware,
        mount: Literal["left", "right"],
    ) -> protocol_api.InstrumentContext:
        return self.protocol.load_instrument(pipette_type, mount, tip_racks=[tiprack])


class OpenTronsProtocol:
    def __init__(self, protocol: protocol_api.ProtocolContext) -> None:
        self.protocol = protocol
        self.labware_loader = LabwareLoader(protocol)

    def exec(self) -> None:
        tiprack = self.labware_loader.get_tiprack("opentrons_96_tiprack_300ul", "7")
        right_pipette = self.labware_loader.load_pipette(
            "p300_multi_gen2", tiprack, "right"
        )
        pool = self.labware_loader.load_plate("corning_96_wellplate_360ul_flat", "6")
        microplate = self.labware_loader.load_plate(
            "corning_96_wellplate_360ul_flat", "2"
        )

        self.perform_pipetting_cycle(
            right_pipette,
            tiprack,
            pool,
            microplate,
        )

    def perform_pipetting_cycle(
        self,
        pipette: protocol_api.InstrumentContext,
        tiprack: protocol_api.labware.Labware,
        pool: protocol_api.labware.Labware,
        plate: protocol_api.labware.Labware,
    ) -> None:
        pipette.pick_up_tip(tiprack.wells_by_name()["A1"])
        for n in range(1, 13):
            pipette.aspirate(150, pool.wells_by_name()["A1"])

            pipette.dispense(150, plate.wells_by_name()[f"A{n}"])

        pipette.drop_tip(tiprack.wells_by_name()["A1"])


def run(protocol: protocol_api.ProtocolContext) -> None:
    ot_protocol = OpenTronsProtocol(protocol)
    ot_protocol.exec()
