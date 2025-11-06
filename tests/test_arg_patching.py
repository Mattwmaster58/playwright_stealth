import pytest
from playwright import async_api
from playwright.async_api import async_playwright

from playwright_stealth import Stealth


@pytest.mark.parametrize("browser_type", ["chromium", "firefox"])
async def test_cli_args_are_patched_correctly(browser_type: str):
    config = Stealth(script_logging=True, navigator_languages_override=("fr-CA", "fr"))
    async with config.use_async(async_playwright()) as ctx:
        browser = await ctx[browser_type].launch()
        page = await browser.new_page()
        console_messages = await collect_log_messages(page)

        await page.goto("http://example.org")
        webdriver_js_was_patched = not any(
            map(lambda x: "not patching navigator.webdriver" in x, console_messages)
        )
        languages_js_was_patched = not any(
            map(lambda x: "not patching navigator.languages" in x, console_messages)
        )
        # iff browser is chromium, we should patch the CLI args
        if browser_type == "chromium":
            assert not webdriver_js_was_patched, console_messages
            assert not languages_js_was_patched, console_messages
        else:
            assert webdriver_js_was_patched, console_messages
            assert languages_js_was_patched, console_messages


async def test_init_scripts_respected():
    # only chromium cli args are instrumented, so no need to check other browsers
    config = Stealth(
        init_scripts_only=True, navigator_languages_override=("fr-CA", "fr")
    )
    async with config.use_async(async_playwright()) as ctx:
        browser = await ctx.chromium.launch()
        page = await browser.new_page()
        console_messages = await collect_log_messages(page)
        languages_js_was_patched = not any(
            map(lambda x: "not patching navigator.languages" in x, console_messages)
        )
        assert languages_js_was_patched


async def collect_log_messages(page):
    console_messages = []

    def collect_log_message(msg: async_api.ConsoleMessage):
        console_messages.append(msg.text)

    page.on("console", collect_log_message)
    return console_messages
