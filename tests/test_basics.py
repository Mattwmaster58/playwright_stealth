import pytest
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

from playwright_stealth.stealth import Stealth, ALL_EVASIONS_DISABLED_KWARGS


@pytest.mark.parametrize("browser_type", ["chromium", "firefox"])
async def test_async_smoketest(browser_type: str):
    # we test this because exceptions won't propagate with page.add_init_scripts, but will with page.evaluate
    async with async_playwright() as p:
        browser = await getattr(p, browser_type).launch()
        page = await browser.new_page()
        await page.goto("http://example.org")
        await page.evaluate(Stealth().script_payload)


@pytest.mark.parametrize("browser_type", ["chromium", "firefox"])
def test_sync_smoketest(browser_type: str):
    with sync_playwright() as p:
        browser = getattr(p, browser_type).launch()
        page = browser.new_page()
        page.goto("http://example.org")
        page.evaluate(Stealth().script_payload)


async def test_async_navigator_webdriver_smoketest(hooked_async_browser):
    for page in [
        await hooked_async_browser.new_page(),
        await (await hooked_async_browser.new_context()).new_page(),
    ]:
        await page.goto("http://example.org")
        assert await page.evaluate("navigator.webdriver") is False


def test_sync_navigator_webdriver_smoketest(hooked_sync_browser):
    for page in [
        hooked_sync_browser.new_page(),
        hooked_sync_browser.new_context().new_page(),
    ]:
        page.goto("http://example.org")
        assert page.evaluate("navigator.webdriver") is False


def test_payload_is_empty_when_no_evasions_active():
    assert len(Stealth(**ALL_EVASIONS_DISABLED_KWARGS).script_payload) == 0


def test_empty_payload_not_injected():
    init_script_added = False

    class MockBrowser:
        def add_init_script(self, *args, **kwargs):
            nonlocal init_script_added
            init_script_added = True

    # noinspection PyTypeChecker
    Stealth(**ALL_EVASIONS_DISABLED_KWARGS).apply_stealth_sync(MockBrowser())
    assert not init_script_added
