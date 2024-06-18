# OpenTronsAPI
[OpenTronsOT-2公式ドキュメント](https://insights.opentrons.com/hubfs/Products/OT-2/OT-2R%20User%20Manual.pdf
)
## Robotとの接続

以下キャリブレーションは完了しているものとする。

1. 背面左のスイッチをON(-)にする。
2. Heartbeat (前面左の青色ランプの点滅が点灯に変わるまで待つ)
3. HEPA moduleをONにする。
4. [OT-2](https://opentrons.com/ot-app/)を起動し、Devicesから下記のデバイスがAvailableになっていることを確認する。この時、Not availableになっている場合は、OT-2およびアプリケーション共に再起動する。

![](docs_images/1.png)

5. デバイスのプレビュー画像をクリックし、下記画面に移動する。
   
![](docs_images/2.png)

6. Lightsトグルからライトの点灯を確認する。(ライト点灯は接続チェックを兼ねる。)

## プロトコルの作成

**本項の最終目標は区画1に配置した300 µLチップを使用して、区画2の溶液を区画3のマイクロプレートに分注し、最後にチップを区画12にドロップすることである。**

### API情報の確認

1. [OpenTrons公式サイト](https://docs.opentrons.com/v2/versioning.html)でAPIバージョンを確認する。本ドキュメントではAPIバージョンを2.11に固定する。
   
2. [OpenTronsLabwares](https://labware.opentrons.com/)からチップのAPIでの名称の確認等を行う。

今回使用するメタデータは以下のように定義する。

```Python

from typing import Annotated, Literal

PipetteType: str = Annotated[str, Literal["p20_multi_gen2", "p300_multi_gen2"]]

metadata: dict[str, str] = {
    "protocolName": "OT-2 Basic Protocol",
    "author": "ikeda042",
    "description": "Basic Protocol for testing",
}

requirements: dict[str, str] = {"robotType": "OT-2", "apiLevel": "2.11"}
```

### セルの名称と位置

ロボットアームの移動は下記のように大きく12区画に分割されており、API呼び出し時に区画を番号で指定する必要がある。

![](docs_images/3.png)

また、チップの位置も下記のように定義されている。

![](docs_images/4.png)

### チップラックの配置

今回は下記のように区画1に`300µL Tip Rack`を配置する。

![](docs_images/tutorial1-1.jpeg)

ここで、ロボットアームに取り付けられたPipetteTypeを下記画面から確かめる。今回は、`300µL Tip Rack`に対応するタイプは`P300 8-channel GEN2`であるため、`Right Mount`を使用して操作を行う。

![](docs_images/tutorial1-2.png)

