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


class Messenger:
    def __init__(self, protocol: protocol_api.ProtocolContext) -> None:
        self.protocol = protocol

    def send_message(self, message: str) -> None:
        url = (
            "http://localhost:8000/send_message"
            if self.protocol.is_simulating()
            else "http://10.32.17.122:8000/send_message"
        )
        try:
            response = requests.post(url, json={"message": message})
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

    @staticmethod
    def get_current_time() -> str:
        return datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S")


class OpenTronsProtocol:
    def __init__(self, protocol: protocol_api.ProtocolContext) -> None:
        self.protocol = protocol
        self.labware_loader = LabwareLoader(protocol)
        self.messenger = Messenger(protocol)

    def exec(self) -> None:
        tiprack = self.labware_loader.get_tiprack("opentrons_96_tiprack_300ul", "7")
        tiprack_2 = self.labware_loader.get_tiprack("opentrons_96_tiprack_20ul", "8")
        right_pipette = self.labware_loader.load_pipette(
            "p300_multi_gen2", tiprack, "right"
        )
        left_pipette = self.labware_loader.load_pipette(
            "p20_multi_gen2", tiprack_2, "left"
        )
        pool = self.labware_loader.load_plate("corning_96_wellplate_360ul_flat", "6")
        pool2 = self.labware_loader.load_plate("corning_96_wellplate_360ul_flat", "4")
        microplate = self.labware_loader.load_plate(
            "corning_96_wellplate_360ul_flat", "2"
        )
        microplate_2 = self.labware_loader.load_plate(
            "corning_96_wellplate_360ul_flat", "1"
        )

        self.messenger.send_message(
            f"*{self.messenger.get_current_time()}* 分注操作を開始します。"
        )

        for i in range(5):
            self.perform_pipetting_cycle(
                right_pipette,
                left_pipette,
                tiprack,
                tiprack_2,
                pool,
                pool2,
                microplate,
                microplate_2,
            )
        self.messenger.send_message(
            f"*{self.messenger.get_current_time()}* 全ての処理が完了しました。"
        )

    def perform_pipetting_cycle(
        self,
        right_pipette: protocol_api.InstrumentContext,
        left_pipette: protocol_api.InstrumentContext,
        tiprack: protocol_api.labware.Labware,
        tiprack_2: protocol_api.labware.Labware,
        pool: protocol_api.labware.Labware,
        pool2: protocol_api.labware.Labware,
        plate: protocol_api.labware.Labware,
        plate_2: protocol_api.labware.Labware,
    ) -> None:
        right_pipette.pick_up_tip(tiprack.wells_by_name()["A1"])
        left_pipette.pick_up_tip(tiprack_2.wells_by_name()["A1"])
        self.messenger.send_message(
            f"*{self.messenger.get_current_time()}* 区画7のラックの1列目からチップを取りました。"
        )
        for n in range(1, 13):
            right_pipette.aspirate(150, pool.wells_by_name()["A1"])
            self.messenger.send_message(
                f"*{self.messenger.get_current_time()}* 区画6の培地プールから8つのピペット全てに150uLの培地を吸引しました。"
            )

            left_pipette.aspirate(20, pool2.wells_by_name()["A1"])
            self.messenger.send_message(
                "*{self.messenger.get_current_time()}* 区画6の培地プールから2つのピペット全てに50uLの培地を吸引しました。"
            )

            right_pipette.dispense(100, plate.wells_by_name()[f"A{n}"])
            self.messenger.send_message(
                f"*{self.messenger.get_current_time()}* 区画2のマイクロプレートリーダーの{n}列目の全ウェルに150uLの溶液を移動しました。"
            )

            left_pipette.dispense(15, plate_2.wells_by_name()[f"A{n}"])
            self.messenger.send_message(
                f"*{self.messenger.get_current_time()}* 区画1のマイクロプレートリーダーの{n}列目の全ウェルに50uLの溶液を移動しました。"
            )

            left_pipette.dispense(5, plate_2.wells_by_name()[f"A{n}"])
            self.messenger.send_message(
                f"*{self.messenger.get_current_time()}* 区画1のマイクロプレートリーダーの{n}列目の全ウェルに30uLの溶液を移動しました。"
            )

            right_pipette.dispense(50, plate_2.wells_by_name()[f"A{n}"])
            self.messenger.send_message(
                f"*{self.messenger.get_current_time()}* 区画1のマイクロプレートリーダーの{n}列目の全ウェルに50uLの溶液を移動しました。"
            )

            right_pipette.drop_tip(tiprack.wells_by_name()["A1"])
            self.messenger.send_message(
                f"*{self.messenger.get_current_time()}* チップを区画7のラックの1列目に戻しました。"
            )

            left_pipette.drop_tip(tiprack_2.wells_by_name()["A1"])
            self.messenger.send_message(
                f"*{self.messenger.get_current_time()}* チップを区画8のラックの1列目に戻しました。"
            )


def run(protocol: protocol_api.ProtocolContext) -> None:
    ot_protocol = OpenTronsProtocol(protocol)
    ot_protocol.exec()
