from opentrons import protocol_api
import requests

# OT-2のIPアドレスとポート番号
ROBOT_IP = "169.254.216.225"
ROBOT_PORT = "31950"

# metadata
metadata = {
    "protocolName": "My Protocol",
    "author": "ikeda042",
    "description": "Simple protocol to demonstrate OT-2 control",
    "apiLevel": "2.11",
}


def run(protocol: protocol_api.ProtocolContext):
    plate = protocol.load_labware("corning_96_wellplate_360ul_flat", "2")
    tiprack = protocol.load_labware("opentrons_96_tiprack_300ul", "1")
    pipette = protocol.load_instrument("p300_multi_gen2", "right", tip_racks=[tiprack])

    pipette.pick_up_tip()
    pipette.aspirate(100, plate["A1"])
    pipette.dispense(100, plate["B1"])
    pipette.drop_tip()


if __name__ == "__main__":
    # プロトコルAPIの取得
    from opentrons.execute import get_protocol_api

    protocol = get_protocol_api("2.11")

    # プロトコルの実行
    run(protocol)

    # OT-2に接続してプロトコルを送信
    url = f"http://{ROBOT_IP}:{ROBOT_PORT}/sessions"
    headers = {"Opentrons-Version": "2"}

    protocol_data = protocol.get_data()  # ここでプロトコルデータを取得
    response = requests.post(url, json=protocol_data, headers=headers)

    if response.status_code == 201:
        print("Protocol successfully uploaded to the robot.")
    else:
        print(f"Failed to upload protocol. Status code: {response.status_code}")
        print(response.json())
