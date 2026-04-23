from __future__ import annotations

import json
from pathlib import Path

CONFIG_PATH = Path("config.json")

DEFAULT_CONFIG = {
    "hotels": [
        {
            "name": "AQUARIUS",
            "url": "https://booking.profitroom.com/pl/hotelaquariusspa/pricelist/rooms/?currency=PLN",
        },
        {
            "name": "HAVET",
            "url": "https://booking.profitroom.com/pl/havethotelresortspadzwirzyno1/pricelist/rooms/?currency=PLN",
        },
        {
            "name": "GRAND",
            "url": "https://booking.profitroom.com/pl/grandlubiczuzdrowiskoustka3/pricelist/rooms/?currency=PLN",
        },
    ],
    "dates": {
        "check_in": "2026-05-11",
        "check_out": "2026-05-14",
    },
}


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)

    data.setdefault("hotels", DEFAULT_CONFIG["hotels"])
    data.setdefault("dates", DEFAULT_CONFIG["dates"])
    data["dates"].setdefault("check_in", DEFAULT_CONFIG["dates"]["check_in"])
    data["dates"].setdefault("check_out", DEFAULT_CONFIG["dates"]["check_out"])
    return data


def save_config(config: dict) -> None:
    with CONFIG_PATH.open("w", encoding="utf-8") as file:
        json.dump(config, file, ensure_ascii=False, indent=2)
