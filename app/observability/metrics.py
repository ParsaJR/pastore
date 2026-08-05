import base64

from prometheus_client import Counter

HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "route", "status"],
)

PASTES_CREATED = Counter(
    "pastore_pastes_created_total",
    "Total pastes created so far",
)


class Metrics_Basic_Auth_ASGIMiddleware:
    """An middleware specially tailored toward the basic_auth mechanism for the metrics endpoint."""
    def __init__(self, app, username: str, password: str):
        self.app = app
        self.username = username
        self.password = password

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        authorization = None

        if not self.username or not self.password:
            await self.app(scope, receive, send)


        for key, value in scope["headers"]:
            if key == b"authorization":
                authorization = value.decode()
                break

        if not authorization or not self.is_authenticated(authorization):
            await self.unauthorized(send)
            return

        await self.app(scope, receive, send)

    async def unauthorized(self, send):
        await send(
            {
                "type": "http.response.start",
                "status": 401,
                "headers": [
                    (
                        b"www-authenticate",
                        b'Basic realm="metrics"',
                    )
                ],
            }
        )

        await send(
            {
                "type": "http.response.body",
                "body": b"Unauthorized",
            }
        )


    def is_authenticated(self, authorization: str) -> bool:
        try:
            scheme, credentials = authorization.split(" ", 1)

            if scheme.lower() != "basic":
                return False

            decoded = base64.b64decode(credentials).decode()

            username, password = decoded.split(":", 1)

            return (
                username == self.username
                and password == self.password
            )

        except (ValueError, UnicodeDecodeError):
            return False
