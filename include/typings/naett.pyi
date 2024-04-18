from typing import Literal

class Response:
    completed: bool
    status_code: int
    text: str
    content: bytes

    headers: dict[str, str]

    def json(self) -> dict: ...

    def __iter__(self) -> Response: ...
    def __next__(self) -> None: ...

def request(
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"],
        url: str,
        headers=None,
        body: str | bytes = None,
        timeout=None) -> Response:
    """Send an HTTP request via non-blocking I/O."""
