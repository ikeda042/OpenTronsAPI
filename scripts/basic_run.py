from opentrons import protocol_api

metadata = {
    "protocolName": "OT-2 Basic Protocol",
    "author": "ikeda042",
    "description": "Basic Protocol for testing",
    "apiLevel": "2.11",
}


def run(protocol: protocol_api.ProtocolContext):
    plate = protocol.load_labware("corning_96_wellplate_360ul_flat", "1")
    tray = protocol.load_labware("corning_96_wellplate_360ul_flat", "6")
    tray2 = protocol.load_labware("corning_96_wellplate_360ul_flat", "4")
    plate_2 = protocol.load_labware("corning_96_wellplate_360ul_flat", "2")
    tiprack = protocol.load_labware("opentrons_96_tiprack_300ul", "7")

    right_pipette = protocol.load_instrument(
        "p300_multi_gen2", "right", tip_racks=[tiprack]
    )

    tiprack2 = protocol.load_labware("opentrons_96_tiprack_20ul", "8")
    left_pipette = protocol.load_instrument(
        "p20_multi_gen2", "left", tip_racks=[tiprack]
    )

    for i in range(50):
        right_pipette.pick_up_tip(tiprack.wells_by_name()["A4"])
        left_pipette.pick_up_tip(tiprack2.wells_by_name()["A1"])
        for i in range(4):
            right_pipette.aspirate(200, tray[f"A{i%12+4}"])
            left_pipette.aspirate(20, tray2[f"A{i%12+4}"])
            right_pipette.dispense(220, tray2[f"A{i%12+4}"])
            left_pipette.dispense(25, tray[f"A{i%12+4}"])
        for i in range(4):
            right_pipette.aspirate(200, tray2[f"A{i%12+4}"])
            left_pipette.aspirate(20, tray[f"A{i%12+4}"])
            right_pipette.dispense(220, tray[f"A{i%12+4}"])
            left_pipette.dispense(25, tray2[f"A{i%12+4}"])
        right_pipette.drop_tip(tiprack.wells_by_name()["A1"])
        left_pipette.drop_tip(tiprack2.wells_by_name()["A1"])
