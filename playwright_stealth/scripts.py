from pathlib import Path
from typing import Dict


def from_file(name) -> str:
    return (Path(__file__).parent / "js" / name).read_text()


SCRIPTS: Dict[str, str] = {
    "generate_magic_arrays": from_file("generate.magic.arrays.js"),
    "utils": from_file("utils.js"),
    "chrome_app": from_file("evasions/chrome.app.js"),
    "chrome_csi": from_file("evasions/chrome.csi.js"),
    "chrome_hairline": from_file("evasions/chrome.hairline.js"),
    "chrome_load_times": from_file("evasions/chrome.load.times.js"),
    "chrome_runtime": from_file("evasions/chrome.runtime.js"),
    "iframe_content_window": from_file("evasions/iframe.contentWindow.js"),
    "media_codecs": from_file("evasions/media.codecs.js"),
    "navigator_hardware_concurrency": from_file("evasions/navigator.hardwareConcurrency.js"),
    "navigator_languages": from_file("evasions/navigator.languages.js"),
    "navigator_permissions": from_file("evasions/navigator.permissions.js"),
    "navigator_platform": from_file("evasions/navigator.platform.js"),
    "navigator_plugins": from_file("evasions/navigator.plugins.js"),
    "navigator_user_agent": from_file("evasions/navigator.userAgent.js"),
    "navigator_vendor": from_file("evasions/navigator.vendor.js"),
    "navigator_webdriver": from_file("evasions/navigator.webdriver.js"),
    "webgl_vendor": from_file("evasions/webgl.vendor.js"),
}

__all__ = ["SCRIPTS"]
