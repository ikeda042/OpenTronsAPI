# OpenTronsAPI

## Robotとの接続

以下キャリブレーションは完了しているものとする。

1. 背面左のスイッチをON(-)にする。
2. Heartbeat (前面左の青色ランプの点滅が点灯に変わるまで待つ)
3. HEPA moduleをONにする。
4. [OT-2](https://opentrons.com/ot-app/)を起動し、Devicesから下記のデバイスがAvailableになっていることを確認する。この時、Not availableになっている場合は、robot、アプリケーション共に再起動する。

![](docs_images/1.png)

5. デバイスのプレビュー画像をクリックし、下記画面に移動する。
   
![](docs_images/2.png)

6. Lightsトグルからライトの点灯を確認する。(ライト点灯は接続チェックを兼ねる。)

## プロトコルの作成

1. [OpenTrons公式サイト](https://docs.opentrons.com/v2/versioning.html)でAPIバージョンを確認する。
   
2. [OpenTronsLabwares](https://labware.opentrons.com/)から
