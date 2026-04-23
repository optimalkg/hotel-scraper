from __future__ import annotations

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError


def handle_popups(page: Page) -> None:
    """Best-effort popup cleanup sequence repeated twice."""
    for _ in range(2):
        try:
            page.get_by_role("button", name="ZAAKCEPTUJ WSZYSTKIE").first.click(timeout=1500)
        except PlaywrightTimeoutError:
            pass

        close_selectors = [
            "button[aria-label='Zamknij']",
            "button[aria-label='Close']",
            "button[class*='close']",
            "[data-testid='close']",
            ".modal button:has-text('×')",
        ]
        for selector in close_selectors:
            try:
                page.locator(selector).first.click(timeout=1200)
            except PlaywrightTimeoutError:
                continue

        page.keyboard.press("Escape")
