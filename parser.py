from __future__ import annotations

from playwright.sync_api import Page


def parse_hotel_data_stub(page: Page, hotel_name: str) -> dict:
    """
    STUB for future parsing logic.

    TODO (next stage):
    - find room cards
    - separate RACK vs package offers
    - normalize prices and availability
    """
    title = page.title()
    return {
        "hotel": hotel_name,
        "status": "stub",
        "page_title": title,
        "rack_price": None,
        "package_price": None,
        "notes": "Placeholder row. Detailed room/offer parsing to be implemented.",
    }
