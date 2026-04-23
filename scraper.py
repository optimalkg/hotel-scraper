from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

from excel_writer import append_result, init_workbook
from parser import parse_hotel_data_stub
from popup_handler import handle_popups

PAGE_TIMEOUT_MS = 60_000
RETRIES = 1
PAUSE_BETWEEN_HOTELS_SECONDS = 2


def build_url_with_dates(base_url: str, check_in: str, check_out: str) -> str:
    parsed = urlparse(base_url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query["check-in"] = check_in
    query["check-out"] = check_out
    updated_query = urlencode(query)
    return urlunparse(parsed._replace(query=updated_query))


def click_apply_if_present(page) -> None:
    candidates = [
        page.get_by_role("button", name="ZASTOSUJ"),
        page.get_by_text("ZASTOSUJ", exact=True),
        page.locator("button:has-text('ZASTOSUJ')"),
    ]
    for candidate in candidates:
        try:
            candidate.first.click(timeout=1500)
            return
        except PlaywrightTimeoutError:
            continue


def analyze_hotel(page, hotel: dict, check_in: str, check_out: str) -> dict:
    url = build_url_with_dates(hotel["url"], check_in, check_out)
    page.goto(url, wait_until="domcontentloaded", timeout=PAGE_TIMEOUT_MS)

    handle_popups(page)
    click_apply_if_present(page)
    handle_popups(page)

    result = parse_hotel_data_stub(page, hotel["name"])
    result["check_in"] = check_in
    result["check_out"] = check_out
    result["url"] = url
    return result


def run_analysis(config: dict) -> dict:
    hotels = config.get("hotels", [])
    check_in = config.get("dates", {}).get("check_in")
    check_out = config.get("dates", {}).get("check_out")

    init_workbook()

    processed = 0
    errors = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.set_default_timeout(PAGE_TIMEOUT_MS)

        for hotel in hotels:
            attempt = 0
            success = False
            while attempt <= RETRIES and not success:
                try:
                    row = analyze_hotel(page, hotel, check_in, check_out)
                    append_result(row)  # intermediate save after each hotel
                    processed += 1
                    success = True
                except Exception as error:  # noqa: BLE001 - keep broad for MVP resiliency
                    attempt += 1
                    if attempt > RETRIES:
                        errors.append({"hotel": hotel.get("name"), "error": str(error)})

            page.wait_for_timeout(PAUSE_BETWEEN_HOTELS_SECONDS * 1000)

        context.close()
        browser.close()

    return {
        "processed_hotels": processed,
        "failed_hotels": len(errors),
        "errors": errors,
    }
