from opentrons import protocol_api
from typing import Literal
import requests
from datetime import datetime, timedelta, timezone

JST: timezone = timezone(timedelta(hours=+9))

metadata = {
    "protocolName": "Base Distributor",
    "author": "ikeda042",
    "description": "分注プロトコル(リザーバーから)",
    "apiLevel": "2.18",
}
