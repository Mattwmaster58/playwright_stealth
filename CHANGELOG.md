2.0.0
 - __breaking change__: more consistent parameter names for the Stealth object
 - new methods to hook context: Stealth.use_async and Stealth.use_sync
    - this allows us to patch CLI options as well, which are often better at faking than JS
 - chore: name options consistently
 - fix: scripts will not crash if in headful mode f9f84861
 - ft: use replaceProperty util which copies existing property descriptors 2b9b4b39
 - fix: remove deprecated pkg_resources usage (to support Python 3.12) (#2)
 - fix: navigator_platform typo (#1)
 - ft: better type hinted functions