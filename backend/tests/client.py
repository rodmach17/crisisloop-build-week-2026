import anyio
import httpx


class ASGITestClient:
    """Small synchronous wrapper around HTTPX's supported ASGI transport."""

    def __init__(self, app) -> None:
        self.app = app

    def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        async def send_request() -> httpx.Response:
            transport = httpx.ASGITransport(app=self.app)
            async with httpx.AsyncClient(
                transport=transport,
                base_url="http://testserver",
            ) as client:
                return await client.request(method, url, **kwargs)

        return anyio.run(send_request)

    def get(self, url: str, **kwargs) -> httpx.Response:
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs) -> httpx.Response:
        return self.request("POST", url, **kwargs)

