from opentrons import protocol_api
from typing import Literal
import requests
from datetime import datetime, timedelta, timezone
import time

JST: timezone = timezone(timedelta(hours=+9))

metadata = {
    "protocolName": "Microplate 96-well Multiple Dilution Protocol",
    "author": "ikeda042",
    "description": "希釈シーケンスを行うプロトコル",
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

    def sleep_for(self, seconds: int) -> None:
        self.messenger.send_message(
            f"*{self.messenger.get_current_time()} ステータス-sleep→* {seconds}秒間シーケンスを中断します。"
        )
        time.sleep(seconds)

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
            f"*{self.messenger.get_current_time()}* シーケンスを開始します。"
        )

        self.messenger.send_message(
            f"*{self.messenger.get_current_time()} メタデータ→* protocol:{metadata['protocolName']},"
            f" author:{metadata['author']}, description:{metadata['description']}, apiLevel:{metadata['apiLevel']}"
        )

        self.perform_pipetting_cycle(
            right_pipette,
            left_pipette,
            tiprack,
            tiprack_2,
            pool,
            pool2,
            microplate,
        )

        self.messenger.send_message(
            f"*{self.messenger.get_current_time()} シーケンス終了* 全ての処理が完了しました。"
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
    ) -> None:

        right_pipette.pick_up_tip(tiprack.wells_by_name()["A6"])
        self.messenger.send_message(
            f"*{self.messenger.get_current_time()} ステータス→* 区画7のラックの6列目から300µLチップを取りました。"
        )

        self.sleep_for(5)

        self.messenger.send_message(
            f"*{self.messenger.get_current_time()} ステータス→* DW20ulを全てのウェルにロードします。"
        )
        # 90ulを全ウェルにロードする
        for n in range(1, 13):
            right_pipette.aspirate(75, pool.wells_by_name()["A1"])
            right_pipette.dispense(75, plate.wells_by_name()[f"A{n}"])
            right_pipette.blow_out()
        self.messenger.send_message(
            f"*{self.messenger.get_current_time()} ステータス→* DW20ulを全てのウェルにロードしました。"
        )

        right_pipette.drop_tip(tiprack.wells_by_name()["A6"])
        self.messenger.send_message(
            f"*{self.messenger.get_current_time()} ステータス→* 区画7のラックの6列目に300µLチップを戻しました。"
        )

        right_pipette.pick_up_tip(tiprack.wells_by_name()["A7"])
        self.messenger.send_message(
            f"*{self.messenger.get_current_time()} ステータス→* 区画7のラックの7列目から300µLチップを取りました。"
        )

        self.messenger.send_message(
            f"*{self.messenger.get_current_time()} ステータス→* 希釈シーケンスを開始します。"
        )

        right_pipette.aspirate(75, pool2.wells_by_name()["A1"])
        right_pipette.dispense(75, plate.wells_by_name()["A1"])
        right_pipette.mix(repetitions=3, volume=50)
        right_pipette.blow_out()

        for i in range(1, 12):
            right_pipette.aspirate(75, plate.wells_by_name()[f"A{i}"])
            right_pipette.dispense(75, plate.wells_by_name()[f"A{i+1}"])
            right_pipette.mix(repetitions=3, volume=50)
            right_pipette.blow_out()

        right_pipette.drop_tip(tiprack.wells_by_name()["A7"])
        self.messenger.send_message(
            f"*{self.messenger.get_current_time()} ステータス→* 区画7のラックの7列目に300µLチップを戻しました。"
        )
        self.messenger.send_message(
            f"*{self.messenger.get_current_time()} ステータス→* 希釈シーケンスが完了しました。"
        )

        # left_pipette.pick_up_tip(tiprack_2.wells_by_name()["A3"])
        # self.messenger.send_message(
        #     f"*{self.messenger.get_current_time()} ステータス→* 区画8のラックの4列目から20µLチップを取りました。"
        # )

        # left_pipette.aspirate(20, pool2.wells_by_name()["A1"])
        # left_pipette.dispense(20, plate.wells_by_name()["A1"])
        # left_pipette.mix(repetitions=3, volume=10)
        # left_pipette.blow_out()

        # self.messenger.send_message(
        #     f"*{self.messenger.get_current_time()} ステータス→* 希釈シーケンスを開始します。"
        # )

        # for n in range(1, 12):
        #     left_pipette.aspirate(20, plate.wells_by_name()[f"A{n}"])
        #     left_pipette.dispense(20, plate.wells_by_name()[f"A{n+1}"])
        #     left_pipette.mix(repetitions=3, volume=10)
        #     left_pipette.blow_out()

        # self.messenger.send_message(
        #     f"*{self.messenger.get_current_time()} ステータス→* 希釈シーケンスが完了しました。"
        # )
        # left_pipette.drop_tip(tiprack_2.wells_by_name()["A3"])

        # self.messenger.send_message(
        #     f"*{self.messenger.get_current_time()} ステータス→* 区画8のラックの3列目に20µLチップを戻しました。"
        # )


def run(protocol: protocol_api.ProtocolContext) -> None:
    ot_protocol = OpenTronsProtocol(protocol)
    ot_protocol.exec()
