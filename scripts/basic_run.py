from opentrons import protocol_api

metadata = {
    "protocolName": "OT-2 Basic Protocol",
    "author": "ikeda042",
    "description": "Basic Protocol for testing",
    "apiLevel": "2.11",
}


def run(protocol: protocol_api.ProtocolContext):
    plate = protocol.load_labware("corning_96_wellplate_360ul_flat", "1")
    tiprack = protocol.load_labware("opentrons_96_tiprack_300ul", "8")
    right_pipette = protocol.load_instrument(
        "p300_multi_gen2", "right", tip_racks=[tiprack]
    )
    for i in range(12):
        right_pipette.pick_up_tip(tiprack.wells_by_name()["A1"])
        right_pipette.aspirate(100, plate[f"A{i%12+1}"])
        right_pipette.dispense(100, plate[f"A{i%12+1}"])
    right_pipette.drop_tip(tiprack.wells_by_name()["A1"])
