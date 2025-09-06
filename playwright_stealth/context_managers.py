from typing import TYPE_CHECKING

from playwright import async_api, sync_api

if TYPE_CHECKING:
    from .stealth import Stealth

# pyright: reportPrivateImportUsage=false


class AsyncWrappingContextManager:
    def __init__(self, stealth: "Stealth", manager: async_api.PlaywrightContextManager):
        if isinstance(manager, sync_api.PlaywrightContextManager):
            raise TypeError("You need to call 'use_sync' instead of 'use_async' for a sync Playwright context")
        self.stealth = stealth
        self.manager = manager

    async def __aenter__(
        self,
    ) -> async_api.Playwright:
        context = await self.manager.__aenter__()
        self.stealth.hook_playwright_context(context)
        return context

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.manager.__aexit__(exc_type, exc_val, exc_tb)


class SyncWrappingContextManager:
    def __init__(self, stealth: "Stealth", manager: sync_api.PlaywrightContextManager):
        if isinstance(manager, async_api.PlaywrightContextManager):
            raise TypeError("You need to call 'use_async' instead of 'use_sync' for an async Playwright context")
        self.stealth = stealth
        self.manager = manager

    def __enter__(
        self,
    ) -> sync_api.Playwright:
        context = self.manager.__enter__()
        self.stealth.hook_playwright_context(context)
        return context

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.manager.__exit__(exc_type, exc_val, exc_tb)


__all__ = ["AsyncWrappingContextManager", "SyncWrappingContextManager"]
