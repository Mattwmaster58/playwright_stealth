from playwright.async_api import async_playwright

from playwright_stealth import Stealth


# todo: more rigorous testing
# these tests aren't useless, because they do actually call injected getters which may eg crash
# but we should probably test they return the values they are supposed to


async def test_chrome_app(hooked_async_page):
    await hooked_async_page.goto("http://example.org")
    a = await hooked_async_page.evaluate("window.chrome")
    b = await hooked_async_page.evaluate("window.chrome.app")


async def test_chrome_csi(hooked_async_page):
    await hooked_async_page.goto("http://example.org")
    a = await hooked_async_page.evaluate("window.chrome.csi")


async def test_chrome_hairline(hooked_async_page):
    await hooked_async_page.goto("http://example.org")
    a = await hooked_async_page.evaluate("document.offsetHeight")


async def test_chrome_load_times(hooked_async_page):
    await hooked_async_page.goto("http://example.org")
    a = await hooked_async_page.evaluate("window.chrome.loadTimes")


async def test_chrome_runtime():
    # disabled by default
    async with Stealth(chrome_runtime=True).use_async(async_playwright()) as p:
        page = await (await p.chromium.launch()).new_page()
        await page.goto("https://example.org")
        a = await page.evaluate("window.chrome.runtime")


async def test_iframe_contentWindow(hooked_async_page):
    await hooked_async_page.goto("http://example.org")
    a = await hooked_async_page.evaluate("document.createElement('iframe')")


async def test_media_codecs(hooked_async_page):
    await hooked_async_page.goto("http://example.org")
    a = await hooked_async_page.evaluate(
        "document.createElement('video').canPlayType('audio/x-m4a')"
    )


async def test_navigator_hardwareConcurrency(hooked_async_page):
    await hooked_async_page.goto("http://example.org")
    a = await hooked_async_page.evaluate("navigator.hardwareConcurrency")


async def test_navigator_languages(hooked_async_page):
    await hooked_async_page.goto("http://example.org")
    a = await hooked_async_page.evaluate("navigator.languages")


async def test_navigator_permissions(hooked_async_page):
    await hooked_async_page.goto("http://example.org")
    a = await hooked_async_page.evaluate("navigator.permissions")


async def test_navigator_platform(hooked_async_page):
    await hooked_async_page.goto("http://example.org")
    a = await hooked_async_page.evaluate("navigator.platform")


async def test_navigator_plugins(hooked_async_page):
    await hooked_async_page.goto("http://example.org")
    a = await hooked_async_page.evaluate("navigator.plugins")


async def test_navigator_userAgent(hooked_async_page):
    await hooked_async_page.goto("http://example.org")
    a = await hooked_async_page.evaluate("navigator.userAgent")


async def test_navigator_vendor(hooked_async_page):
    await hooked_async_page.goto("http://example.org")
    a = await hooked_async_page.evaluate("navigator.vendor")


async def test_navigator_webdriver(hooked_async_page):
    await hooked_async_page.goto("http://example.org")
    a = await hooked_async_page.evaluate("navigator.webdriver")


async def test_webgl_vendor(hooked_async_page):
    await hooked_async_page.goto("http://example.org")
    a = await hooked_async_page.evaluate("WebGLRenderingContext.getParameter")
    b = await hooked_async_page.evaluate("WebGL2RenderingContext.getParameter")
