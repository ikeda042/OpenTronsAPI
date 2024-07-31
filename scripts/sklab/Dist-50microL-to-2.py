from opentrons import protocol_api
from typing import Literal
from datetime import timedelta, timezone
from typing import Annotated

Jst: timezone = timezone(timedelta(hours=+9))
Slot = Annotated[
    Literal["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
    "value should be between 1 and 12",
]
PlateIndex = Annotated[
    Literal["4", "5", "7", "8", "10", "11"],
    "value should be in the list",
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
    "description": "分注プロトコル(リザーバーからスロット２に50マイクロずつ分注)",
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


## Base settings
plates_to_use: list[int] = [2]
dist_amounts: list[int] = [50]
plates_to_use: list[PlateIndex] = [str(i) for i in plates_to_use]


class Dist50to2:
    def __init__(
        self,
        protocol: protocol_api.ProtocolContext,
        plates_to_use: list[PlateIndex],
        dist_amounts: list[int],
    ) -> None:
        labware_loader: LabwareLoader = LabwareLoader(protocol)
        self.tiprack: protocol_api.labware.Labware = labware_loader.get_tiprack(
            "opentrons_96_tiprack_300ul", "9"
        )
        self.right_pipette: protocol_api.InstrumentContext = (
            labware_loader.load_pipette("p300_multi_gen2", self.tiprack, "right")
        )
        self.right_pipette.default_speed = 450

        self.reservoir: protocol_api.labware.Labware = labware_loader.load_plate(
            "corning_96_wellplate_360ul_flat", "1"
        )
        self.microplates: list[protocol_api.labware.Labware] = [
            labware_loader.load_plate("corning_96_wellplate_360ul_flat", slot)
            for slot in plates_to_use
        ]
        self.plates_to_use: list[PlateIndex] = plates_to_use
        self.dist_amounts: list[int] = dist_amounts
        if len(plates_to_use) != len(dist_amounts):
            raise ValueError(
                "The length of plates_to_use and dist_amounts must be the same."
            )

    def distribute(self, aspirate_height_in_mm: float | None = 10.0) -> None:
        self.right_pipette.pick_up_tip(self.tiprack.wells_by_name()["A2"])
        for n, j in enumerate(self.dist_amounts):
            for w in range(1, 2):
                for i in range(3):
                    self.right_pipette.aspirate(
                        j,
                        self.reservoir.wells_by_name()["A7"].bottom(
                            aspirate_height_in_mm
                        ),
                    )
                    self.right_pipette.dispense(
                        j,
                        self.reservoir.wells_by_name()[f"A7"].bottom(
                            aspirate_height_in_mm
                        ),
                    )
                    self.right_pipette.blow_out()
                self.right_pipette.aspirate(
                    50,
                    self.reservoir.wells_by_name()["A7"].bottom(aspirate_height_in_mm),
                )
                self.right_pipette.dispense(
                    50,
                    self.microplates[n].wells_by_name()[f"A{w}"],
                )
                self.right_pipette.blow_out()
        # self.right_pipette.drop_tip(self.tiprack.wells_by_name()["A1"])
        self.right_pipette.drop_tip()


def run(protocol: protocol_api.ProtocolContext) -> None:
    ot_protocol = Dist50to2(protocol, plates_to_use, dist_amounts)
    ot_protocol.distribute(aspirate_height_in_mm=5.0)
