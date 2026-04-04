import json

from playwright.async_api import async_playwright

from playwright_stealth import Stealth


async def test_navigator_user_agent_data_brands_no_headless(hooked_async_chromium_page):
    """Test that HeadlessChrome is not in navigator.userAgentData.brands"""
    await hooked_async_chromium_page.goto("https://example.org")
    brands = await hooked_async_chromium_page.evaluate("navigator.userAgentData.brands")
    for brand in brands:
        assert brand["brand"] != "HeadlessChrome", "HeadlessChrome should not be in brands"


async def test_navigator_user_agent_data_disabled():
    """Test that the evasion can be disabled"""
    async with Stealth(navigator_user_agent_data=False, navigator_user_agent=False).use_async(async_playwright()) as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://example.org")
        assert "HeadlessChrome" in json.dumps(await page.evaluate("navigator.userAgentData.toJSON()"))


async def test_navigator_user_agent_data_toJSON(hooked_async_chromium_page):
    """Test that toJSON filters HeadlessChrome"""
    await hooked_async_chromium_page.goto("https://example.org")
    json_data = await hooked_async_chromium_page.evaluate("navigator.userAgentData.toJSON()")
    for brand in json_data["brands"]:
        assert brand["brand"] != "HeadlessChrome", "HeadlessChrome should not be in toJSON output"
    assert "mobile" in json_data, "toJSON should include mobile property"
    assert "platform" in json_data, "toJSON should include platform property"


async def test_navigator_user_agent_data_getHighEntropyValues(hooked_async_chromium_page):
    """Test that getHighEntropyValues filters HeadlessChrome"""
    await hooked_async_chromium_page.goto("https://example.org")

    # Test with brands hint
    data = await hooked_async_chromium_page.evaluate("navigator.userAgentData.getHighEntropyValues(['brands'])")
    if "brands" in data:
        for brand in data["brands"]:
            assert brand["brand"] != "HeadlessChrome", "HeadlessChrome should not be in high entropy brands"

    # Test with fullVersionList hint
    data = await hooked_async_chromium_page.evaluate(
        "navigator.userAgentData.getHighEntropyValues(['fullVersionList'])"
    )
    if "fullVersionList" in data:
        for brand in data["fullVersionList"]:
            assert brand["brand"] != "HeadlessChrome", "HeadlessChrome should not be in fullVersionList"


async def test_navigator_user_agent_data_preserves_mobile_platform(hooked_async_chromium_page):
    """Test that mobile and platform properties are preserved"""
    await hooked_async_chromium_page.goto("https://example.org")
    mobile = await hooked_async_chromium_page.evaluate("navigator.userAgentData.mobile")
    platform = await hooked_async_chromium_page.evaluate("navigator.userAgentData.platform")
    assert isinstance(mobile, bool), "mobile should be a boolean"
    assert isinstance(platform, str), "platform should be a string"
    assert len(platform) > 0, "platform should not be empty"


# Smoketests (basic execution test)
async def test_navigator_user_agent_data_smoketest(hooked_async_chromium_page):
    """Smoketest: basic execution without errors"""
    await hooked_async_chromium_page.goto("https://example.org")
    # Just access the property to ensure no errors
    ua_data = await hooked_async_chromium_page.evaluate("navigator.userAgentData")
    brands = await hooked_async_chromium_page.evaluate("navigator.userAgentData.brands")
    toJSON = await hooked_async_chromium_page.evaluate("navigator.userAgentData.toJSON()")
    # Test getHighEntropyValues (returns a Promise, need to await in JS)
    high_entropy = await hooked_async_chromium_page.evaluate(
        "navigator.userAgentData.getHighEntropyValues(['brands', 'mobile', 'platform'])"
    )
