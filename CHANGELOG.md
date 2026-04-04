# 2.0.3

- Added `navigator.userAgentData` evasion (PR #28 - thanks [@straywarrior](https://github.com/straywarrior))

# 2.0.2

- Fixed wrapper compatibility with wrapped classes in context managers (PR #27 - thanks [@tobbber](https://github.com/tobbber))

# 2.0.1

- Added guard against double application of stealth (warns and skips duplicate applications)
- Relaxed playwright dependency to `>=1.40.0`
- [internal]: use poetry v2+ format for pyproject.tml (PR #23 - thanks [@Rafiot](https://github.com/Rafiot))
- Added `error_prototype` evasion to override Error.name (PR #22 - thanks [@Rafiot](https://github.com/Rafiot))
- Added handler variable name randomization in `utils.stripProxyFromErrors` for better stealth (PR #18 - thanks [@Rafiot](https://github.com/Rafiot))

# 2.0.0

- __breaking change__: more consistent naming all around
- __breaking change__: Stealth object only takes kwargs now
- new methods to hook context: Stealth.use_async and Stealth.use_sync
    - this allows us to patch CLI options as well, which are often better at faking than JS
- chore: name options consistently
- fix: scripts will not crash if in headful mode f9f84861
- ft: use replaceProperty util which copies existing property descriptors 2b9b4b39
- fix: remove deprecated pkg_resources usage (to support Python 3.12) (#2)
- fix: navigator_platform typo (#1)
- ft: better type hinted functions
- ft: User-Agent and Sec-CH-UA spoofing
- chore: remove chrome.run_on_unsecure_origins option (didn't see a purpose)
- ft: sane navigator.platform default override
