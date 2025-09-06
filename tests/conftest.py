import pytest
from playwright import async_api, sync_api
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

from playwright_stealth import Stealth

script_logging = True
browser_types = ["chromium", "firefox"]


@pytest.fixture(params=browser_types)
async def hooked_async_browser(request) -> async_api.Browser:
    async with Stealth(script_logging=script_logging).use_async(
        async_playwright()
    ) as ctx:
        browser = await ctx[request.param].launch()
        yield browser


@pytest.fixture(params=browser_types)
def hooked_sync_browser(request) -> sync_api.Browser:
    with Stealth(script_logging=script_logging).use_sync(sync_playwright()) as ctx:
        browser = ctx[request.param].launch()
        yield browser


@pytest.fixture
async def hooked_async_page(hooked_async_browser) -> async_api.Page:
    return await hooked_async_browser.new_page()


@pytest.fixture
def hooked_sync_page(request, hooked_async_browser) -> sync_api.Page:
    return hooked_async_browser.new_page()
