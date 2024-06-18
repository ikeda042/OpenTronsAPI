from opentrons import protocol_api
from typing import Literal
import requests

metadata = {
    "protocolName": "OT-2 Basic Protocol",
    "author": "ikeda042",
    "description": "Basic Protocol for testing",
    "apiLevel": "2.18",
}


class OpenTronsProtocol:
    def __init__(self, protocol: protocol_api.ProtocolContext) -> None:
        self.protocol: protocol_api.ProtocolContext = protocol
        self.analysis_mode: bool = protocol.is_simulating()

    def get_tiprack(
        self,
        protocol: protocol_api.ProtocolContext,
        tiprack_type: Literal[
            "opentrons_96_tiprack_300ul", "opentrons_96_tiprack_20ul"
        ],
        slot: Literal["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
    ) -> protocol_api.labware.Labware:
        return protocol.load_labware(tiprack_type, slot)

    def load_plate(
        self,
        protocol: protocol_api.ProtocolContext,
        plate_type: Literal["corning_96_wellplate_360ul_flat"],
        slot: Literal["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
    ) -> protocol_api.labware.Labware:
        return protocol.load_labware(plate_type, slot)

    def load_pipette(
        self,
        protocol: protocol_api.ProtocolContext,
        pipette_type: Literal["p300_multi_gen2", "p20_multi_gen2"],
        tiprack: protocol_api.labware.Labware,
        mount: Literal["left", "right"],
    ) -> protocol_api:
        return protocol.load_instrument(pipette_type, mount, tip_racks=[tiprack])

    def exec(
        self,
    ) -> None:
        tiprack = self.get_tiprack(self.protocol, "opentrons_96_tiprack_300ul", "7")
        right_pipette = self.protocol.load_instrument(
            "p300_multi_gen2", "right", tip_racks=[tiprack]
        )
        plate_1 = self.load_plate(self.protocol, "corning_96_wellplate_360ul_flat", "6")

        for i in range(3):
            right_pipette.pick_up_tip(tiprack.wells_by_name()["A1"])
            self.send_message(
                "区画7のラックの1列目のチップを取りました。(8チャンネルピペット)"
            )
            right_pipette.aspirate(200, plate_1.wells_by_name()["A1"])
            self.send_message("1列目の全ウェルから200uLの溶液を吸引しました。")
            right_pipette.dispense(200, plate_1.wells_by_name()["A2"])
            self.send_message("2列目の全ウェルに200uLの溶液を移動しました。")
            right_pipette.drop_tip(tiprack.wells_by_name()["A1"])
            self.send_message("チップを区画7のラックの1列目に戻しました。")
        self.send_message("全ての処理が完了しました。")

    @staticmethod
    def send_message(message: str) -> None:
        try:
            response = requests.post(
                "http://10.32.17.122:8000/send_message", json={"message": message}
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        return None


def run(protocol: protocol_api.ProtocolContext) -> None:
    ot = OpenTronsProtocol(protocol)
    ot.exec()
