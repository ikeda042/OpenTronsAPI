from opentrons import protocol_api


class BasicRunProtocol:
    def __init__(self) -> None:
        self.metadata = {
            "protocolName": "Basic Protocol",
            "author": "ikeda042",
            "description": "Basic Protocol for testing",
        }
        self.requirements = {"apiLevel": "2.11"}


# protocol run function
def run(protocol: protocol_api.ProtocolContext):
    # labware
    plate = protocol.load_labware("corning_96_wellplate_360ul_flat", location="D1")
    tiprack = protocol.load_labware("opentrons_flex_96_tiprack_200ul", location="D2")
    trash = protocol.load_trash_bin(location="A3")

    # pipettes
    left_pipette = protocol.load_instrument(
        "flex_1channel_1000", mount="left", tip_racks=[tiprack]
    )

    # commands
    left_pipette.pick_up_tip()
    left_pipette.aspirate(100, plate["A1"])
    left_pipette.dispense(100, plate["B2"])
    left_pipette.drop_tip()
