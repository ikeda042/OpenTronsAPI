from opentrons import protocol_api
from datetime import timedelta, timezone
from enum import Enum

JST: timezone = timezone(timedelta(hours=+9))

metadata = {
    "protocolName": "Microplate 96-well Protocol",
    "author": "ikeda042",
    "description": "Basic Protocol for testing",
    "apiLevel": "2.18",
}


class TiprackType(Enum):
    OPENTRONS_96_TIPRACK_300UL = "opentrons_96_tiprack_300ul"
    OPENTRONS_96_TIPRACK_20UL = "opentrons_96_tiprack_20ul"


class PlateType(Enum):
    CORNING_96_WELLPLATE_360UL_FLAT = "corning_96_wellplate_360ul_flat"


class PipetteType(Enum):
    P300_MULTI_GEN2 = "p300_multi_gen2"
    P20_MULTI_GEN2 = "p20_multi_gen2"


class MountType(Enum):
    LEFT = "left"
    RIGHT = "right"


class Slot(Enum):
    SLOT_1 = "1"
    SLOT_2 = "2"
    SLOT_3 = "3"
    SLOT_4 = "4"
    SLOT_5 = "5"
    SLOT_6 = "6"
    SLOT_7 = "7"
    SLOT_8 = "8"
    SLOT_9 = "9"
    SLOT_10 = "10"
    SLOT_11 = "11"


class Colunm(Enum):
    Colunm_1 = "1"
    Colunm_2 = "2"
    Colunm_3 = "3"
    Colunm_4 = "4"
    Colunm_5 = "5"
    Colunm_6 = "6"
    Colunm_7 = "7"
    Colunm_8 = "8"
    Colunm_9 = "9"
    Colunm_10 = "10"
    Colunm_11 = "11"
    Colunm_12 = "12"


class Row(Enum):
    Row_A = "A"
    Row_B = "B"
    Row_C = "C"
    Row_D = "D"
    Row_E = "E"
    Row_F = "F"
    Row_G = "G"
    Row_H = "H"


class LabwareLoader:
    def __init__(self, protocol: protocol_api.ProtocolContext) -> None:
        self.protocol = protocol

    def get_tiprack(
        self,
        tiprack_type: TiprackType,
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
        pipette_type: PipetteType,
        tiprack: protocol_api.labware.Labware,
        mount: MountType,
    ) -> protocol_api.InstrumentContext:
        return self.protocol.load_instrument(pipette_type, mount, tip_racks=[tiprack])


class OpenTronsProtocol:
    def __init__(self, protocol: protocol_api.ProtocolContext) -> None:
        self.protocol = protocol
        self.labware_loader = LabwareLoader(protocol)

    def exec(self) -> None:
        tiprack = self.labware_loader.get_tiprack(
            TiprackType.OPENTRONS_96_TIPRACK_300UL, Slot.SLOT_7
        )
        right_pipette = self.labware_loader.load_pipette(
            PipetteType.P300_MULTI_GEN2, tiprack, "right"
        )
        pool = self.labware_loader.load_plate(
            PlateType.CORNING_96_WELLPLATE_360UL_FLAT, Slot.SLOT_6
        )
        microplate = self.labware_loader.load_plate(
            PlateType.CORNING_96_WELLPLATE_360UL_FLAT, Slot.SLOT_2
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
