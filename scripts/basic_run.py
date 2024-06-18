from opentrons import protocol_api, types
from opentrons import simulate, execute


# class OT2BasicProtocol:
#     def __init__(self) -> None:
#         self.metadata = {
#             "protocolName": "Basic Protocol",
#             "author": "ikeda042",
#             "description": "Basic Protocol for testing",
#         }
#         self.requirements = {"robotType": "OT-2", "apiLevel": "2.18"}
#         self.

# PipetteType: str = Annotated[str, Literal["p20_multi_gen2", "p300_multi_gen2"]]
# MountType: str = Annotated[str, Literal["left", "right"]]

metadata: dict[str, str] = {
    "protocolName": "OT-2 Basic Protocol",
    "author": "ikeda042",
    "description": "Basic Protocol for testing",
}

requirements: dict[str, str] = {"robotType": "OT-2", "apiLevel": "2.11"}


def run(protocol: protocol_api.ProtocolContext):
    plate = protocol.load_labware("corning_96_wellplate_360ul_flat", "2")
    tiprack = protocol.load_labware("opentrons_96_tiprack_300ul", "1")
    right_pipette = protocol.load_instrument(
        "p300_multi_gen2", "right", tip_racks=[tiprack]
    )

    right_pipette.pick_up_tip(tiprack.wells_by_name()["A1"])
    right_pipette.aspirate(100, plate["A1"])
    right_pipette.dispense(100, plate["B2"])
    right_pipette.drop_tip(tiprack.wells_by_name()["B12"])
