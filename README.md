# playwright_stealth

Transplanted from [puppeteer-extra-plugin-stealth](https://github.com/berstend/puppeteer-extra/tree/master/packages/puppeteer-extra-plugin-stealth), with some improvements. Don't expect this to bypass anything but the simplest of bot detection methods. Consider this a proof-of-concept starting point.

This is a WIP fork. I've merged some of the outstanding PRs and added some features with the goal of replacing the out-of-date upstream. See the [changelog](./README.md).

## Install

Install the latest stable release:
```
$ pip install git+https://github.com/Mattwmaster58/playwright_stealth@rc4
```
or straight from `main`
```
$ pip install git+https://github.com/Mattwmaster58/playwright_stealth
```

## Example Usage

### Recommended Usage
```python
import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def main():
    # This is the recommended usage. All pages created will have stealth applied:
    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        webdriver_status = await page.evaluate("navigator.webdriver")
        print("from new_page: ", webdriver_status)
        
        different_context = await browser.new_context()
        page_from_different_context = await different_context.new_page()

        different_context_status = await page_from_different_context.evaluate("navigator.webdriver")
        print("from new_context: ", different_context_status)

asyncio.run(main())
```

### Specifying config options and applying evasions manually to an entire context
```python
import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth, ALL_EVASIONS_DISABLED_KWARGS

async def advanced_example():
    # Custom configuration with specific languages
    custom_languages = ("fr-FR", "fr")
    stealth = Stealth(
        navigator_languages_override=custom_languages,
        init_scripts_only=True
    )
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        await stealth.apply_stealth_async(context)
        
        # Test stealth on multiple pages
        page_1 = await context.new_page()
        page_2 = await context.new_page()
        
        # Verify language settings
        for i, page in enumerate([page_1, page_2], 1):
            is_mocked = await page.evaluate("navigator.languages") == custom_languages
            print(f"Stealth applied to page {i}: {is_mocked}")

    # Example of selective evasion usage
    no_evasions = Stealth(**ALL_EVASIONS_DISABLED_KWARGS)
    single_evasion = Stealth(**{**ALL_EVASIONS_DISABLED_KWARGS, "navigator_webdriver": True})
    
    print("Total evasions (none):", len(no_evasions.script_payload))
    print("Total evasions (single):", len(single_evasion.script_payload))

asyncio.run(advanced_example())
```

## Todo
 - make this work with playwright.launch_persistent_context
 - sec-platform (we have navigator_play)
 - docs

## A set of Test results

### playwright with stealth

![playwright without stealth](./images/example_with_stealth.png)

### playwright without stealth

![playwright with stealth](./images/example_without_stealth.png)
